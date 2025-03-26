"""Models for reading related features"""
from django.db import models
from users.models import User
from main.models import GraphicTitle, TextTitle, GraphicTitleChapter, TextTitleChapter


class GraphicTitleView(models.Model):
    """Allows tracking views for graphic titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(GraphicTitle, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class TextTitleView(models.Model):
    """Allows tracking views for text titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    
class GraphicTitleFavorite(models.Model):
    """Allows tracking favorites count for graphic titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(GraphicTitle, on_delete=models.CASCADE)


class TextTitleFavorite(models.Model):
    """Allows tracking favorites count for text titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE)
    
    
class GraphicTitleBookmark(models.Model):
    """Tracking bookmarks for graphic titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(GraphicTitle, on_delete=models.CASCADE)
    chapter = models.ForeignKey(GraphicTitleChapter, on_delete=models.CASCADE)

class TextTitleBookmark(models.Model):
    """Tracking bookmarks for text titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE)
    chapter = models.ForeignKey(TextTitleChapter, on_delete=models.CASCADE)