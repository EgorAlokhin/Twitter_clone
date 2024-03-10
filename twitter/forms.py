from django import forms
from .models import Tweet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Tweet_form(forms.ModelForm):
    body = forms.CharField(required = True, widget = forms.widgets.Textarea(
        attrs = {'placeholder': 'Enter Your Tweet', 'class' : 'form-control'}), label = '')

    class Meta:
        model = Tweet
        exclude = ('author', 'likes')

class Sign_up_form(UserCreationForm):
    email = forms.EmailField(label = '', widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label = '', max_length=20, widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Your Name'}))
    last_name = forms.CharField(label = '', max_length=20, widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Your Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(Sign_up_form, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='User Name'
        self.fields['username'].label=''
        self.fields['username'].help_text='<span class = "form-text text-muted"><small>No more than 150 symbols</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class = "form-text text-muted"><small>No less than 8 symbols, should contain letters and numbers</small></span>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Reenter Your password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class = "form-text text-muted"><small>Enter Your password again</small></span>'

class Profile_image_form(forms.ModelForm):
    profile_img = forms.ImageField(label = 'Profile image')
    profile_bio = forms.CharField(label='Profile Bio', widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Profile Bio'}))
    facebook_link = forms.CharField(label='Facebook Link', widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Facebook link'}))
    instagram_link = forms.CharField(label='Instagram link', widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Instagram link'}))
    class Meta:
        model = Profile
        fields = ('profile_img', 'profile_bio', 'facebook_link', 'instagram_link')