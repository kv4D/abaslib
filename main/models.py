"""
Models for 'main' app. Basically models for content and
some functions for convenience.
"""
import os
from django.db import models



def get_graphic_chapter_path(instance, filename):
    """Creates the path to the chapter of a graphic title"""
    # if there is no title in eng, use russian
    title_name = instance.chapter.title.title_name_eng
    if not title_name:
        title_name = instance.chapter.title.title_name_rus
    # formatting title to some_title_name
    title_name = title_name.lower().replace(' ', '_')
    return os.path.join('graphic', title_name, 'chapters', instance.chapter.chapter_name, filename)


def get_text_chapter_path(instance, filename):
    """Creates the path to the chapter of a text title"""
    # if there is no title in eng, use russian
    title_name = instance.title.title_name_eng
    if not title_name:
        title_name = instance.title.title_name_rus
    # formatting title to some_title_name
    title_name = title_name.lower().replace(' ', '_')
    return os.path.join('text', title_name, 'chapters', instance.chapter_name, filename)


# Create your models here.
class Title(models.Model):
    """
    Represents a basic title model and its common attributes both
    for graphic and text content
    """
    title_name_rus = models.CharField(max_length=255)
    title_name_eng = models.CharField(max_length=255)
    title_author = models.CharField(max_length=255)
    title_description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title_name_eng}/{self.title_name_rus}'


class TextTitle(Title):
    """A title with text only"""
    # for specification purposes
    pass


class GraphicTitle(Title):
    """A comic title or manga only"""
    # for specification purposes
    pass


class TextTitleChapter(models.Model):
    """Represents a chapter from a certain text title"""
    # access title's chapters with obj.chapters.all()
    title = models.ForeignKey(TextTitle, on_delete=models.CASCADE, related_name='chapters')     
    chapter_name = models.CharField(max_length=255)
    # a file with the chapter's content
    text_content = models.FileField(upload_to=get_text_chapter_path)

    class Meta:
        # chapters are ordered by their ids
        ordering = ["id"]
        
    def __str__(self):
        return f'{self.chapter_name}/{str(self.title)}'


class GraphicTitleChapter(models.Model):
    """Represents a chapter from a certain graphic title"""
    # access title's chapters with obj.chapters.all()
    title = models.ForeignKey(GraphicTitle, on_delete=models.CASCADE, related_name='chapters')
    chapter_name = models.CharField(max_length=255)

    class Meta:
        # chapters are ordered by their ids
        ordering = ["id"]

    def __str__(self):
        return f'{self.chapter_name}/{str(self.title)}'


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
        unique_together = ['chapter', 'page_number']

    def __str__(self):
        return f'{self.page_number}/{str(self.chapter)}'
