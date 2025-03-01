"""For 'main' app's models registration"""
from django.contrib import admin
from . models import TextTitle, GraphicTitle, \
                        TextTitleChapter, GraphicTitleChapter, \
                        GraphicTitlePage


# modifying admin site fields to show
class TextTitleAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)

class GraphicTitleAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)

class TextTitleChapterAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)

class GraphicTitleChapterAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)

# Register your models here.
admin.site.register(TextTitle, TextTitleAdmin)
admin.site.register(GraphicTitle, GraphicTitleAdmin)
admin.site.register(TextTitleChapter, TextTitleChapterAdmin)
admin.site.register(GraphicTitleChapter, GraphicTitleChapterAdmin)
admin.site.register(GraphicTitlePage)
