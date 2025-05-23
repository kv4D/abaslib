"""For 'main' app's models registration"""
from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import gettext_lazy as _
from . models import TextTitle, GraphicTitle, \
                        TextTitleChapter, GraphicTitleChapter, \
                        GraphicTitlePage
from metadata.models import TitleGenre, TitleTag
from ratings.models import TitleRating
                        

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
    
class TitleGenreInline(GenericTabularInline):
    model = TitleGenre
    extra = 1
    ct_field = 'content_type'  
    ct_fk_field = 'object_id'  
    
class TitleRatingInline(GenericTabularInline):
    model = TitleRating
    extra = 1
    ct_field = 'content_type'  
    ct_fk_field = 'object_id'  
    
class TitleTagInline(GenericTabularInline):
    model = TitleTag
    extra = 1
    ct_field = 'content_type'  
    ct_fk_field = 'object_id'  
    
class TextTitleAdmin(admin.ModelAdmin):
    readonly_fields = ('title_cover_preview', 'added_at', 'views_count', 'favorites_count')
    inlines = [TextTitleChapterInline, TitleGenreInline, TitleTagInline, TitleRatingInline]
    
    @admin.display(description=_('Превью обложки'))
    def title_cover_preview(self, title):
        width = title.title_cover.width
        height = title.title_cover.height
        
        return mark_safe(
            f'<img src="{title.title_cover.url}" width="{width}px" height={height}px />'
            )
    
class GraphicTitleAdmin(admin.ModelAdmin):
    readonly_fields = ('title_cover_preview', 'added_at', 'views_count', 'favorites_count')
    inlines = [GraphicTitleChapterInline, TitleGenreInline, TitleTagInline]    
    
    @admin.display(description=_('Превью обложки'))
    def title_cover_preview(self, title):
        width = title.title_cover.width
        height = title.title_cover.height
        
        return mark_safe(
            f'<img src="{title.title_cover.url}" width="{width}px" height={height}px />'
            )
        
class TextTitleChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter_name', 'chapter_number', 'display_number')
    list_filter = ('title', 'display_number')
    readonly_fields = ('added_at',)
    
class GraphicTitleChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter_name', 'chapter_number', 'display_number')
    list_filter = ('title', 'display_number')
    readonly_fields = ('added_at',)
    inlines = [GraphicTitlePageInline]


admin.site.register(TextTitle, TextTitleAdmin)
admin.site.register(GraphicTitle, GraphicTitleAdmin)
admin.site.register(TextTitleChapter, TextTitleChapterAdmin)
admin.site.register(GraphicTitleChapter, GraphicTitleChapterAdmin)
admin.site.register(GraphicTitlePage)
