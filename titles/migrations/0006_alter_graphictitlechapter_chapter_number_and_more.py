# Generated by Django 5.1.7 on 2025-04-13 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0005_alter_graphictitlechapter_chapter_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphictitlechapter',
            name='chapter_number',
            field=models.FloatField(max_length=5),
        ),
        migrations.AlterField(
            model_name='texttitlechapter',
            name='chapter_number',
            field=models.FloatField(max_length=5),
        ),
    ]
