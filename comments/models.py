from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Comment(models.Model):
    user = models.ForeignKey('users.User', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    
    # for any title type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    added_at = models.DateTimeField(auto_now_add=True,
                                    verbose_name=_('Добавлено'))

    class Meta:
        ordering = ['added_at']
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
        
    def __str__(self):
        return f'Comment {self.text[:10]}... by {self.user.username}'