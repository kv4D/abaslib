"""Models for rating system"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType


class TitleRating(models.Model):
    rate = models.FloatField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    # for any title type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rate__range=(1, 5)), name='rate in range 1 to 5'),
            models.UniqueConstraint(fields=['user', 'content_type', 'object_id'], name='rate only once')
        ]
        verbose_name = _('Оценка тайтла')
        verbose_name_plural = _('Оценки тайтлов')
        
    def __str__(self):
        return f'Оценки "{self.content_object}"'
    
    @staticmethod
    def get_average_rate(title):
        """Get average rate for title"""
        avg = TitleRating.objects.filter(
            content_type=ContentType.objects.get_for_model(title),
            object_id=title.id
        ).aggregate(models.Avg('rate'))['rate__avg']
        
        return avg
    
    @staticmethod
    def get_rates_count(title):
        """Get amount of rates for title"""
        count = TitleRating.objects.filter(
            content_type=ContentType.objects.get_for_model(title),
            object_id=title.id
        ).count()
        
        return count
