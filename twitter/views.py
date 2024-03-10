from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import Tweet_form, Sign_up_form, Profile_image_form
from django.contrib.auth import login, logout, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = Tweet_form(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                tweet = form.save(commit = False)
                tweet.author = request.user
                tweet.save()
                messages.success(request, ('Your tweet has been added'))
                return redirect('home')
        tweets = Tweet.objects.all().order_by('-created')
        return render(request, "home.html", {'tweets': tweets, 'form':form})
    else:
        tweets = Tweet.objects.all().order_by('-created')
        return render(request, "home.html", {'tweets':tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request, "profile_list.html", {'profiles':profiles})
    else:
        messages.success(request, ('Please, log in'))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        tweets = Tweet.objects.filter(author_id = pk).order_by('-created')
        if request.method == 'POST':
            current_user = request.user.profile
            action = request.POST['Follow']
            if action == 'follow':
                current_user.follows.add(profile)
            elif action == 'unfollow':
                current_user.follows.remove(profile)
            current_user.save()
        return render(request, "profile.html", {'profile':profile, 'tweets':tweets})
    else:
        messages.success(request, ('Please, log in'))
        return redirect('home')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have logged in'))
            return redirect('home')
        else:
            messages.success(request, ('such user does not existe, please, register'))
            return redirect('home')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have logged out'))
    return redirect('home')

def register_user(request):
    form = Sign_up_form()
    if request.method == 'POST':
        form = Sign_up_form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have signed in'))
            return redirect('home')
        else:
            messages.success(request, ('such user does not existe, please, register'))
            return redirect('home')
    else:
        return render(request, "register.html", {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        profile_user = Profile.objects.get(user__id = request.user.id)
        user_form = Sign_up_form(request.POST or None, instance = current_user)
        profile_form = Profile_image_form(request.POST or None, request.FILES or None, instance = profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ('You profile has been updated'))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ('You must be logged in'))
        return redirect('login')

def like_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id = pk)
        if tweet.likes.filter(id = request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect('home')
    else:
        messages.success(request, ('You must be logged in'))
        return redirect('login')

def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request, ('You have successfully lost a fried, Congrats!'))
        return redirect('home')
    else:
        messages.success(request, ('You must be logged in'))
        return redirect('home')

def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request, ('You have successfully foud a fried, Congrats!'))
        return redirect('home')
    else:
        messages.success(request, ('You must be logged in'))
        return redirect('home')

def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, "followers.html", {'profiles': profiles})
        else:
            messages.success(request, ('This is not Your profile'))
            return redirect('home')
    else:
        messages.success(request, ('Please, log in'))
        return redirect('home')

def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, "followers.html", {'profiles': profiles})
        else:
            messages.success(request, ('This is not Your profile'))
            return redirect('home')
    else:
        messages.success(request, ('Please, log in'))
        return redirect('home')

def delete_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.author.username:
            tweet.delete()
            messages.success(request, ('You have successfully deletd a post'))
            return redirect('home')
        else:
            messages.success(request, ('It is not Your post'))
            return redirect('home')
    else:
        messages.success(request, ('Please, log in'))
        return redirect('home')

def edit_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.author.username:
             form = Tweet_form(request.POST or None, instance=tweet)
             if request.method == 'POST':
                 if form.is_valid():
                     tweet = form.save(commit = False)
                     tweet.author = request.user
                     tweet.save()
                     messages.success(request, ('You have chaged the informtion of the tweet, like The Big Brother'))
                     return redirect('home')
             else:
                return render(request, 'edit_tweet.html', {'form':form, 'tweet':tweet})
        else:
            messages.success(request, ('It is not Your post'))
            return redirect('home')
    else:
        messages.success(request, ('Please, log in'))
        return redirect('home')

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        searched = Tweet.objects.filter(body__contains = search)
        messages.success(request, ('Here is what you searched for'))
        return render(request, 'search.html', {'searched':searched})
    else:
        return render(request, 'search.html', {})