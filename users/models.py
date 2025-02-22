"""
Models for 'main' app. Mostly user related.
"""
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class UserProfile(models.Model):
    '''Extending Django base User model''' 
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    user_avatar = models.ImageField(default='default_avatar.jpg', upload_to='profile_avatars')

    def __str__(self):
        return get_user_model().username
