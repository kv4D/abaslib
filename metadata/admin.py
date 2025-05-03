"""For 'metadata' app's models registration"""
from django.contrib import admin
from . import models
from django.contrib import admin


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['tag_name']
    list_filter = ['tag_name']

@admin.register(models.TagGenre)
class TagGenreAdmin(admin.ModelAdmin):
    list_display = ['tag_name']
    list_filter = ['tag_name']
