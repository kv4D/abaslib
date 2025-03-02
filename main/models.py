"""
Models for 'main' app. Basically models for content and
some functions for convenience.
"""
import os
from django.db import models
from datetime import datetime


def get_graphic_chapter_path(instance, filename):
    """Creates the path to the chapter of a graphic title"""
    # if there is no title in eng, use russian
    title_id = instance.chapter.title.id
    return os.path.join('graphic', str(title_id), 'chapters', instance.chapter.chapter_name, filename)


def get_text_chapter_path(instance, filename):
    """Creates the path to the chapter of a text title"""
    # if there is no title in eng, use russian
    title_id = instance.title.id
    return os.path.join('text', str(title_id), 'chapters', instance.chapter_name, filename)


# Create your models here.
class Title(models.Model):
    """
    Represents a basic title model and its common attributes both
    for graphic and text content
    """
    title_name_rus = models.CharField(max_length=100, unique=True)
    title_name_eng = models.CharField(max_length=100, unique=True)
    title_author = models.CharField(max_length=100)
    title_is_ongoing = models.BooleanField(default=True)
    title_description = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    publication_year = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title_name_eng} / {self.title_name_rus}'


class TextTitle(Title):
    """A title with text only"""
    # for specification purposes
    @property
    def title_type(self):
        return 'text'

class GraphicTitle(Title):
    """A comic title or manga only"""
    # for specification purposes
    @property
    def title_type(self):
        return 'graphic'

class TextTitleChapter(models.Model):
    """Represents a chapter from a certain text title"""
    # access title's chapters with obj.chapters.all()
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE, related_name='chapters')     
    chapter_name = models.CharField(max_length=255)
    # a file with the chapter's content
    text_content = models.FileField(upload_to=get_text_chapter_path)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # chapters are ordered by their ids
        ordering = ["id"]
        
    def __str__(self):
        return f'{self.chapter_name} / {str(self.title)}'


class GraphicTitleChapter(models.Model):
    """Represents a chapter from a certain graphic title"""
    # access title's chapters with obj.chapters.all()
    title = models.ForeignKey(GraphicTitle, on_delete=models.CASCADE, related_name='chapters')
    chapter_name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # chapters are ordered by their ids
        ordering = ["id"]

    def __str__(self):
        return f'{self.chapter_name} / {str(self.title)}'


class GraphicTitlePage(models.Model):
    """A page for a graphic title chapter"""
    # access chapters's pages with obj.pages.all()
    chapter = models.ForeignKey(GraphicTitleChapter, on_delete=models.CASCADE,related_name='pages')
    image = models.ImageField(upload_to=get_graphic_chapter_path)
    page_number = models.PositiveIntegerField()

    class Meta:
        # we should sort by page number
        ordering = ['page_number']
        # one page №(some number) for a chapter
        constraints = [
        models.UniqueConstraint(fields=['chapter', 'page_number'], name='unique_page_per_chapter')]

    def __str__(self):
        return f'{self.page_number} / {str(self.chapter)}'
