"""
Models for 'main' app. Mostly user related.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import TextTitle, GraphicTitle


# Create your models here.
class User(AbstractUser):
    '''Extending Django base User model''' 
    user_avatar = models.ImageField(default='default_avatar.jpg', upload_to='profile_avatars')
    titles_read_amount = models.IntegerField(default=0)
    favorite_text_titles = models.ManyToManyField(TextTitle, blank=True)
    favorite_graphic_titles = models.ManyToManyField(GraphicTitle, blank=True)
    
    def likes_title(self, title: TextTitle | GraphicTitle):
        return self.favorite_text_titles.filter(id=title.id).exists() or self.favorite_graphic_titles.filter(id=title.id).exists()