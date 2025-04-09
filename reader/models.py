"""Models for reading related features"""
from django.db import models
from users.models import User
from main.models import GraphicTitle, TextTitle, GraphicTitleChapter, TextTitleChapter


class GraphicTitleFavorite(models.Model):
    """Tracking which user has a graphic title in favorites"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='graphic_favorites')
    title = models.ForeignKey(GraphicTitle, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_favorite_count(title):
        """Count all views for this title (unauthorized users included)"""
        count = GraphicTitleFavorite.objects.filter(title=title).count()
        return count


class TextTitleFavorite(models.Model):
    """Tracking which user has a text title in favorites"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='text_favorites')
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.title}'

    @staticmethod
    def get_favorite_count(title):
        """Count all users with provided title in favorites"""
        count = TextTitleFavorite.objects.filter(title=title).count()
        return count


class GraphicTitleView(models.Model):
    """Allows tracking views for graphic titles"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name='graphic_viewed'
                             )
    title = models.ForeignKey(
        GraphicTitle,
        on_delete=models.CASCADE,
        related_name='graphic_viewers'
        )
    user_ip = models.CharField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.title}'

    @staticmethod
    def get_views_count(title):
        """Count all users with provided title in favorites"""
        count = GraphicTitleView.objects.filter(title=title).count()
        return count


class TextTitleView(models.Model):
    """Allows tracking views for text titles"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name='text_viewed'
                             )
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE, related_name='text_viewers')
    user_ip = models.CharField()
    time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_views_count(title):
        """Count all views for this title (unauthorized users included)"""
        count = TextTitleView.objects.filter(title=title).count()
        return count


class GraphicTitleBookmark(models.Model):
    """Tracking bookmarks for graphic titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='graphic_bookmarks')
    title = models.ForeignKey(GraphicTitle, on_delete=models.CASCADE)
    chapter = models.ForeignKey(GraphicTitleChapter, on_delete=models.CASCADE)


class TextTitleBookmark(models.Model):
    """Tracking bookmarks for text titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='text_bookmarks')
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE)
    chapter = models.ForeignKey(TextTitleChapter, on_delete=models.CASCADE)
