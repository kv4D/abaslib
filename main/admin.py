"""For 'main' app's models registration"""
from django.contrib import admin
from . models import TextTitle, GraphicTitle, \
                        TextTitleChapter, GraphicTitleChapter, \
                        GraphicTitlePage


# modifying admin site fields to show
class TextTitleChapterInline(admin.TabularInline):
    model = TextTitleChapter
    extra = 1

class TextTitleAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)
    inlines = [TextTitleChapterInline]

class GraphicTitleChapterInline(admin.TabularInline):
    model = GraphicTitleChapter
    extra = 1

class GraphicTitleAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)
    inlines = [GraphicTitleChapterInline]

class TextTitleChapterAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)
    
class GraphicTitlePageInline(admin.TabularInline):
    model = GraphicTitlePage
    extra = 1

class GraphicTitleChapterAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)
    inlines = [GraphicTitlePageInline]

# Register your models here.
admin.site.register(TextTitle, TextTitleAdmin)
admin.site.register(GraphicTitle, GraphicTitleAdmin)
admin.site.register(TextTitleChapter, TextTitleChapterAdmin)
admin.site.register(GraphicTitleChapter, GraphicTitleChapterAdmin)
admin.site.register(GraphicTitlePage)
