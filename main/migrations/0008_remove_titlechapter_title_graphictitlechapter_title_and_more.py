# Generated by Django 5.1.6 on 2025-03-05 18:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_graphictitle_title_name_eng_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='titlechapter',
            name='title',
        ),
        migrations.AddField(
            model_name='graphictitlechapter',
            name='title',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='graphic_chapters', to='main.graphictitle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='texttitlechapter',
            name='title',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='text_chapters', to='main.texttitle'),
            preserve_default=False,
        ),
    ]
