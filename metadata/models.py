"""Models for metadata about titles"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType


class TitleFavorite(models.Model):
    """Tracking which user has a title in favorites"""
    user = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             related_name='favorite_titles'
                             )
    
    # for any title type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'content_type')
        verbose_name = _('Избранное')
        verbose_name_plural = _('Избранное')
    
    def __str__(self):
        return f"{self.user} - {self.content_object}"
    
    @staticmethod
    def get_favorite_count(title):
        """Count all views for this title (unauthorized users included)"""
        count = TitleFavorite.objects.filter(
            content_type=ContentType.objects.get_for_model(title),
            object_id=title.id
            ).count()
        return count
    
    @staticmethod
    def get_favorite_status(title, user):
        """Try to get favorite status"""
        try:
            status = TitleFavorite.objects.filter(
                content_type=ContentType.objects.get_for_model(title),
                user=user
                ).exists()
        except TypeError:
            # anonymous user, no status
            status = None
        return status
    

class TitleView(models.Model):
    """Tracking views for titles"""
    user = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name='viewed_titles'
                             )
    user_ip = models.CharField()
    
    # for any title type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'content_type')
        verbose_name = _('Просмотр')
        verbose_name_plural = _('Просмотры')
    
    def __str__(self):
        return f"{self.user} - {self.content_object}"
    
    @staticmethod
    def get_views_count(title):
        """Count all views for this title (unauthorized users included)"""
        count = TitleView.objects.filter(
            content_type=ContentType.objects.get_for_model(title),
            object_id=title.id
            ).count()
        return count
    

class Tag(models.Model):
    """Tag for special information about titles"""
    tag_name = models.CharField(verbose_name='Имя тэга', max_length=100, unique=True)
    
    class Meta:
        verbose_name = _('Тэг')
        verbose_name_plural = _('Тэги')
        ordering = ['tag_name']
        
    def __str__(self):
        return f"{self.tag_name}"
    
    
class TagGenre(models.Model):
    """Tag for title genres only"""
    tag_name = models.CharField(verbose_name='Название жанра', max_length=100, unique=True)
    
    class Meta:
        verbose_name = _('Тэг-жанр')
        verbose_name_plural = _('Тэги-жанры')
        ordering = ['tag_name']
    
    def __str__(self):
        return f"{self.tag_name}"
    
    
class TitleGenre(models.Model):
    """Titles and genres relation"""
    tag_genre = models.ForeignKey(TagGenre, on_delete=models.CASCADE)
    
    # for any title type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = _('Жанр тайтла')
        verbose_name_plural = _('Жанры тайтлов')
    
    def __str__(self):
        return f"{self.content_object} - {self.tag_genre}"
    
    @staticmethod
    def get_all_title_genres(title):
        content_type = ContentType.objects.get_for_model(title)
        genres = TitleGenre.objects.filter(
            content_type=content_type,
            object_id=title.id
            )
        return genres
    
    
class TitleTag(models.Model):
    """Titles and tags relation"""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    # for any title type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = _('Тэг тайтла')
        verbose_name_plural = _('Тэги тайтлов')
    
    def __str__(self):
        return f"{self.content_object} - {self.tag}"
    
    @staticmethod
    def get_all_title_tags(title):     
        content_type = ContentType.objects.get_for_model(title)
        tags = TitleTag.objects.filter(
            content_type=content_type,
            object_id=title.id
            )
        return tags