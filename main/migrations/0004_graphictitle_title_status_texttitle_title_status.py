# Generated by Django 5.1.5 on 2025-03-01 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_graphictitlechapter_added_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphictitle',
            name='title_status',
            field=models.CharField(default='ongoing', max_length=40),
        ),
        migrations.AddField(
            model_name='texttitle',
            name='title_status',
            field=models.CharField(default='ongoing', max_length=40),
        ),
    ]
