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
    title_name_eng = models.CharField(max_length=100, unique=True, blank=True)
    title_author = models.CharField(max_length=100)
    title_is_ongoing = models.BooleanField(default=True)
    title_description = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    publication_year = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title_name_rus} ({self.title_name_eng})'


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
        models.UniqueConstraint(fields=['chapter_name', 'chapter_number'], name='unique_chapter_per_title')]

    def get_chapter_name(self):
        return f'Глава {self.chapter_number} - {self.chapter_name}'
    
    def __str__(self):
        return f'Глава {self.chapter_number} - {self.chapter_name} / {str(self.title)}'
    

class TextTitleChapter(TitleChapter):
    """Represents a chapter from a certain text title"""
    # a file with the chapter's content
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE, related_name='text_chapters')     
    text_content = models.FileField(upload_to=get_text_chapter_path)
    
    # for specification purposes
    @property
    def title_type(self):
        return 'text'


class GraphicTitleChapter(TitleChapter):
    """Represents a chapter from a certain graphic title"""
    # for specification purposes
    title = models.ForeignKey(GraphicTitle, on_delete=models.CASCADE, related_name='graphic_chapters')     
    
    @property
    def title_type(self):
        return 'graphic'


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
