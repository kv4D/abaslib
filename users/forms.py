"""Contains forms for 'users' app"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """Registration form for UserProfile"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
