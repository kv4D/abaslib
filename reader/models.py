"""Models for reading related features"""
from django.db import models


class Bookmark(models.Model):
    """Abstract model for bookmarks"""
    user = models.ForeignKey('users.User', 
                             on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
        unique_together = ('user', 'title')
        
    def __str__(self):
        return f"{self.user} - {self.chapter} ({self.title})"

class GraphicTitleBookmark(Bookmark):
    """Tracking bookmarks for graphic titles"""
    title = models.ForeignKey('titles.GraphicTitle', on_delete=models.CASCADE)
    chapter = models.ForeignKey('titles.GraphicTitleChapter', on_delete=models.CASCADE)
    page = models.ForeignKey('titles.GraphicTitlePage', 
                             on_delete=models.CASCADE, 
                             blank=True, 
                             null=True)
    
    @staticmethod
    def get_user_bookmark_for_title(user, title):
        return GraphicTitleBookmark.objects.filter(user=user, title=title).first()


class TextTitleBookmark(Bookmark):
    """Tracking bookmarks for text titles"""
    title = models.ForeignKey('titles.TextTitle', on_delete=models.CASCADE)
    chapter = models.ForeignKey('titles.TextTitleChapter', on_delete=models.CASCADE)
    
    @staticmethod
    def get_user_bookmark_for_title(user, title):
        return TextTitleBookmark.objects.filter(user=user, title=title).first()