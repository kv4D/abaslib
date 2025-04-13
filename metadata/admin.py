"""For 'metadata' app's models registration"""
from django.contrib import admin
from . import models
from django.contrib import admin

admin.site.register(models.Tag)
admin.site.register(models.TagGenre)
