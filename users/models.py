"""
Models for 'main' app. Mostly user related.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import TextTitle, GraphicTitle


class User(AbstractUser):
    '''Extending Django base User model'''
    user_avatar = models.ImageField(default='default_avatar.jpg', upload_to='profile_avatars')
    titles_read_amount = models.IntegerField(default=0)
    favorite_text_titles = models.ManyToManyField(TextTitle, blank=True)
    favorite_graphic_titles = models.ManyToManyField(GraphicTitle, blank=True)

    def has_title_in_favorites(self, title: TextTitle | GraphicTitle):
        """Checks if user likes title"""
        if title.title_type == 'text':
            return self.favorite_text_titles.filter(id=title.id).exists()
        if title.title_type == 'graphic':
            return self.favorite_graphic_titles.filter(id=title.id).exists()

    def add_title_to_favorites(self, title: TextTitle | GraphicTitle):
        """Adds title to user's favorites"""
        if title.title_type == 'text':
            self.favorite_text_titles.add(title)
        elif title.title_type == 'graphic':
            self.favorite_graphic_titles.add(title)

    def remove_title_from_favorites(self, title: TextTitle | GraphicTitle):
        """Removes title from user's favorites"""
        if title.title_type == 'text':
            self.favorite_text_titles.remove(title)
        elif title.title_type == 'graphic':
            self.favorite_graphic_titles.remove(title)

    def get_bookmark(self, title: TextTitle | GraphicTitle):
        """Provides user's bookmark for title"""
        pass
