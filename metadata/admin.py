"""For 'metadata' app's models registration"""
from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

@admin.register(models.TitleGenre)
class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('tag_genre', 'content_object', 'content_type')
    list_filter = ('tag_genre', 'content_type')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'content_type':
            # Ограничиваем выбор только моделями тайтлов
            kwargs['queryset'] = ContentType.objects.filter(model__in=['texttitle', 'graphictitle'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.TitleFavorite)
admin.site.register(models.TitleView)
admin.site.register(models.Tag)
admin.site.register(models.TagGenre)
admin.site.register(models.TitleTag)
