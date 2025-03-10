"""Contains forms for 'users' app"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """Registration form for User"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        
        help_text = {
            'username': 'help text',
            'password': 'some help text'
        }
