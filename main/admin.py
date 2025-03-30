"""For 'main' app's models registration"""
from django.contrib import admin
from django.utils.html import mark_safe
from . models import TextTitle, GraphicTitle, \
                        TextTitleChapter, GraphicTitleChapter, \
                        GraphicTitlePage
                        

# modifying admin site fields to show
class TextTitleChapterInline(admin.TabularInline):
    model = TextTitleChapter
    extra = 1
    
class GraphicTitleChapterInline(admin.TabularInline):
    model = GraphicTitleChapter
    extra = 1
    
class GraphicTitlePageInline(admin.TabularInline):
    model = GraphicTitlePage
    extra = 1
    
class TextTitleAdmin(admin.ModelAdmin):
    readonly_fields = ('title_cover_preview', 'added_at')
    inlines = [TextTitleChapterInline]
    
    def title_cover_preview(self, title):
        width = title.title_cover.width
        height = title.title_cover.height
        
        return mark_safe(
            f'<img src="{title.title_cover.url}" width="{width}px" height={height}px />'
            )
    
class GraphicTitleAdmin(admin.ModelAdmin):
    readonly_fields = ('title_cover_preview', 'added_at')
    inlines = [GraphicTitleChapterInline]    
    
    def title_cover_preview(self, title):
        width = title.title_cover.width
        height = title.title_cover.height
        
        return mark_safe(
            f'<img src="{title.title_cover.url}" width="{width}px" height={height}px />'
            )
        
class TextTitleChapterAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)
    
class GraphicTitleChapterAdmin(admin.ModelAdmin):
    readonly_fields = ('added_at',)
    inlines = [GraphicTitlePageInline]

# Register your models here.
admin.site.register(TextTitle, TextTitleAdmin)
admin.site.register(GraphicTitle, GraphicTitleAdmin)
admin.site.register(TextTitleChapter, TextTitleChapterAdmin)
admin.site.register(GraphicTitleChapter, GraphicTitleChapterAdmin)
admin.site.register(GraphicTitlePage)
