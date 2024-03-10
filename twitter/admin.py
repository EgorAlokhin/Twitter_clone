from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile, Tweet

# Unregister the default Group model from the admin
admin.site.unregister(Group)
class ProfileInLine(admin.StackedInline):
    model = Profile
# Define the custom UserAdmin class
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInLine]
# Unregister the default User model from the admin
admin.site.unregister(User)

# Register the User model with the custom UserAdmin class
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Profile)

admin.site.register(Tweet)