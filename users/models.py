from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # extending Django base User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    User._meta.get_field('email')._unique = True
    
    user_avatar = models.ImageField(default='default_avatar.jpg', upload_to='profile_images')

    def __str__(self):
        return self.user.username
    