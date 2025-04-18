# Generated by Django 5.1.7 on 2025-04-10 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphictitlechapter',
            name='display_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='graphictitlechapter',
            name='volume',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='texttitlechapter',
            name='display_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='texttitlechapter',
            name='volume',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='graphictitlechapter',
            name='chapter_number',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='texttitlechapter',
            name='chapter_number',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
