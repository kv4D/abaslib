"""
Models for 'main' app. Basically models for content and
some functions for convenience.
"""
import os
from django.db import models
from django.utils import timezone


def get_graphic_chapter_path(instance, filename):
    """Creates the path to the chapter of a graphic title"""
    title_id = instance.chapter.title.id
    return os.path.join(
        'graphic', str(title_id), 'chapters', instance.chapter.chapter_name, filename
        )


def get_text_chapter_path(instance, filename):
    """Creates the path to the chapter of a text title"""
    title_id = instance.title.id
    return os.path.join(
        'text', str(title_id), 'chapters', instance.chapter_name, filename
        )


# Create your models here.
class Title(models.Model):
    """
    Represents a basic title model and its common attributes both
    for graphic and text content
    """
    title_name_rus = models.CharField(max_length=100, unique=True)
    title_name_eng = models.CharField(max_length=100, unique=True, blank=True)
    title_author = models.CharField(max_length=100)
    title_is_ongoing = models.BooleanField(default=True)
    title_description = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    publication_year = models.PositiveSmallIntegerField(default=timezone.now().year)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title_name_rus} ({self.title_name_eng})'


class TextTitle(Title):
    """A title with text only"""
    # for specification purposes
    class Meta:
        constraints = [
                models.CheckConstraint(
                    check=models.Q(publication_year__lte=timezone.now().year) & models.Q(publication_year__gt=0),
                    name='0 < publication year <= current year (text)'
                )
            ]

    def get_path(self):
        """Returns path to title"""
        return os.path.join('media', 'text', str(self.id))

    @property
    def title_type(self):
        """Returns title type"""
        return 'text'

class GraphicTitle(Title):
    """A comic title or manga only"""
    # for specification purposes
    class Meta:
        constraints = [
                models.CheckConstraint(
                    check=models.Q(publication_year__lte=timezone.now().year) & models.Q(publication_year__gt=0),
                    name='0 < publication year <= current year (graphic)'
                )
            ]

    def get_path(self):
        """Returns path to title"""
        return os.path.join('media', 'graphic', str(self.id))

    @property
    def title_type(self):
        """Returns title type"""
        return 'graphic'


class TitleChapter(models.Model):
    """
    Represents a basic title chapter model and its common attributes both
    for graphic and text content
    """
    # access title's chapters with obj.chapters.all()
    chapter_name = models.CharField(max_length=255)
    chapter_number = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # chapters are ordered by their ids
        ordering = ["id"]
        # one chapter for a title
        constraints = [
            models.UniqueConstraint(
                fields=['chapter_name', 'chapter_number'],
                name='unique_chapter_per_title'
                )
            ]

    def __str__(self):
        return f'Глава {self.chapter_number}: {self.chapter_name}'


class TextTitleChapter(TitleChapter):
    """Represents a chapter from a certain text title"""
    # a file with the chapter's content
    title = models.ForeignKey(
        TextTitle,
        on_delete=models.CASCADE,
        related_name='text_chapters'
        )
    text_content = models.FileField(upload_to=get_text_chapter_path)

    def get_path(self):
        """Returns path to chapter"""
        return os.path.join('media', 'text', str(self.title.id), str(self.id))

    @property
    def title_type(self):
        """Returns title type"""
        return 'text'


class GraphicTitleChapter(TitleChapter):
    """Represents a chapter from a certain graphic title"""
    # for specification purposes
    title = models.ForeignKey(
        GraphicTitle,
        on_delete=models.CASCADE,
        related_name='graphic_chapters'
        )

    def get_path(self):
        """Returns path to chapter"""
        return os.path.join('media', 'graphic', str(self.title.id), str(self.id))

    @property
    def title_type(self):
        """Returns title type"""
        return 'graphic'


class GraphicTitlePage(models.Model):
    """A page for a graphic title chapter"""
    # access chapters's pages with obj.pages.all()
    chapter = models.ForeignKey(
        GraphicTitleChapter,
        on_delete=models.CASCADE,
        related_name='pages'
        )
    image = models.ImageField(upload_to=get_graphic_chapter_path)
    page_number = models.PositiveIntegerField()

    class Meta:
        # we should sort by page number
        ordering = ['page_number']
        # one page №(some number) for a chapter
        constraints = [
            models.UniqueConstraint(
                fields=['chapter', 'page_number'],
                name='unique_page_per_chapter'
                )
            ]

    def __str__(self):
        return f'{self.page_number} / {str(self.chapter)}'
