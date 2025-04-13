"""Config for 'users' app"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Config class"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'