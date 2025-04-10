"""For 'metadata' app's models registration"""
from django.contrib import admin
from . import models


admin.site.register(models.TitleFavorite)
admin.site.register(models.TitleView)
admin.site.register(models.Tag)
admin.site.register(models.TagGenre)
admin.site.register(models.TitleGenre)
admin.site.register(models.TitleTag)
