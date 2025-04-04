# Generated by Django 5.1.7 on 2025-03-31 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_graphictitle_title_cover_texttitle_title_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphictitle',
            name='favorites_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='graphictitle',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='texttitle',
            name='favorites_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='texttitle',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
