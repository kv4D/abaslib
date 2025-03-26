"""For 'reader' app's models registration"""
from django.contrib import admin
from . import models


admin.site.register(models.GraphicTitleView)
admin.site.register(models.GraphicTitleBookmark)
admin.site.register(models.GraphicTitleFavorite)
admin.site.register(models.TextTitleView)
admin.site.register(models.TextTitleBookmark)
admin.site.register(models.TextTitleFavorite)
