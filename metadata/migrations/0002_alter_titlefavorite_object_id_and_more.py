# Generated by Django 5.1.7 on 2025-04-13 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titlefavorite',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='titleview',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
    ]
