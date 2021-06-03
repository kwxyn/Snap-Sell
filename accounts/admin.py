from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'avatar'
    ]

admin.site.register(UserProfile, UserProfileAdmin)
