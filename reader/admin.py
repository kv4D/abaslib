"""For 'reader' app's models registration"""
from django.contrib import admin
from . import models


admin.site.register(models.GraphicTitleBookmark)
admin.site.register(models.TextTitleBookmark)
