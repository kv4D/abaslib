"""Contains forms for 'users' app"""
from django import forms
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


class RegisterForm(UserCreationForm):
    """Registration form for User"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        
        labels = {
            'title_name_rus': _('Название тайтла'),
            'title_name_eng': _('Название тайтла (английский, опционально)'), 
            'title_author': _('Автор'), 
            'title_is_ongoing': _('Тайтл все еще выходит'),
            'title_description': _('Описание'), 
            'publication_year': _('Год выпуска')
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_id = 'auth_form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('users:register')
        
        self.helper.add_input(Submit('submit', 'Submit'))
        
        # change labels
        self.fields['username'].label = _('Никнейм')
        self.fields['email'].label = _('Электронная почта')
        self.fields['password1'].label = _('Пароль')
        self.fields['password2'].label = _('Подтверждение пароля')
        
        # change help text
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = _('<br/>Пароль должен содержать хотя бы 8 символов')
        
        # change error messages
        self.fields['username'].error_messages = {
            'required': 'Поле "Имя пользователя" обязательно для заполнения.',
            'unique': 'Пользователь с таким именем уже существует.',
        }
        self.fields['password1'].error_messages = {
            'required': 'Поле "Пароль" обязательно для заполнения.',
        }
        self.fields['password2'].error_messages = {
            'required': 'Поле "Подтверждение пароля" обязательно для заполнения.',
        }
        
        
class LoginForm(AuthenticationForm):    
    class Meta:
        model = get_user_model()
        
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        # build crispy form
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('users:login')
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Войти', css_class='submit_button'),)
        
        # change labels
        self.fields['username'].label = 'Никнейм'
        self.fields['password'].label = 'Пароль'
    
    error_messages = {
        'invalid_login': _('Неверный никнейм или пароль'),
        'inactive': _('Этот аккаунт отключён'),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data