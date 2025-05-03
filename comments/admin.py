from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'added_at']
    list_filter = ['user', 'added_at']