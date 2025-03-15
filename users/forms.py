"""Contains forms for 'users' app"""
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper


class RegisterForm(UserCreationForm):
    """Registration form for User"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # change help text
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = _('Пароль должен содержать хотя бы 8 символов')
        
        #change error messages