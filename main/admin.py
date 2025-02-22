"""For 'main' app's models registration"""
from django.contrib import admin
from . models import TextTitle, GraphicTitle, \
                        TextTitleChapter, GraphicTitleChapter, \
                        GraphicTitlePage


# Register your models here.
admin.site.register(TextTitle)
admin.site.register(GraphicTitle)
admin.site.register(TextTitleChapter)
admin.site.register(GraphicTitleChapter)
admin.site.register(GraphicTitlePage)
