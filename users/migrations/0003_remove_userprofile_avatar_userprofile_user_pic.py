# Generated by Django 5.1.6 on 2025-02-19 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='avatar',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_pic',
            field=models.ImageField(default='base_profile_pic.png', upload_to='profile_images'),
        ),
    ]
