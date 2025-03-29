"""Contains forms for 'users' app"""
from django import forms
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class RegisterForm(UserCreationForm):
    """Registration form for User"""
    email = forms.EmailField(required=True)

    # error messages
    error_messages = {
        'invalid_email': _('Пользователь с такой электронной почтой уже существует'),
    }

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # build crispy form
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('users:register')
        self.helper.layout = Layout(
            'username',
            'email',
            'password1',
            'password2',
            Submit(name='submit', value=_('Зарегистрироваться'), css_class='submit_button'),)

        # change labels
        self.fields['username'].label = _('Никнейм')
        self.fields['email'].label = _('Электронная почта')
        self.fields['password1'].label = _('Пароль')
        self.fields['password2'].label = _('Подтвердите пароль')

        # change help text
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = _('<br>Пароль должен содержать хотя бы 8 символов (из них обязательно 1 символ не цифра)')
        self.fields['password2'].help_text = None

        # change error messages
        self.fields['username'].error_messages = {
            'unique': _('Пользователь с таким именем уже существует'),
        }

    def clean_email(self):
        """Validate email"""
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        email_used = get_user_model().objects.filter(email=email).exclude(username=username).exists()
        if email and email_used:
            raise forms.ValidationError(
                self.error_messages['invalid_email'],
                code='invalid_email',
                )
        return email

class LoginForm(AuthenticationForm):
    """Login form for User"""
    # error messages
    error_messages = {
        'invalid_login': _('Неверный никнейм или пароль'),
        'inactive': _('Этот аккаунт отключён'),
    }

    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # build crispy form
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('users:login')
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', _('Войти'), css_class='submit_button'),)

        # change labels
        self.fields['username'].label = 'Никнейм'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        """Validate form"""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
