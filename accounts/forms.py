from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):

    username = forms.CharField(
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Username'}),
        label = 'Username'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        max_length=32,
        label = 'First Name'

    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        max_length=32,
        label='Last Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
        max_length=64,
        label='Email'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label='Confirm password'
    )
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old password'}),
        label='Old password'
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
        label='New password'
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label='Confirm password'
    )

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
        max_length=32,
        label = 'First name'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
        max_length=32,
        label='Last name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
        max_length=64,
        label='Email'
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")