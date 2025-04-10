"""Models for reading related features"""
from django.db import models
from users.models import User
from titles.models import GraphicTitle, TextTitle, GraphicTitleChapter, TextTitleChapter


class GraphicTitleBookmark(models.Model):
    """Tracking bookmarks for graphic titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='graphic_bookmarks')
    title = models.ForeignKey(GraphicTitle, on_delete=models.CASCADE)
    chapter = models.ForeignKey(GraphicTitleChapter, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'title', 'chapter')
        
    def __str__(self):
        return f"{self.user} - {self.chapter} ({self.title})"


class TextTitleBookmark(models.Model):
    """Tracking bookmarks for text titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='text_bookmarks')
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE)
    chapter = models.ForeignKey(TextTitleChapter, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'title', 'chapter')
        
    def __str__(self):
        return f"{self.user} - {self.chapter} ({self.title})"
