from django.db import models
import os


def get_graphic_chapter_path(instance, filename):
    """Creates the path to the chapter of a graphic book"""
    # if there is no title in eng, use russian
    title = instance.chapter.book.title_eng
    if not title:
        title = instance.chapter.book.title_rus
    
    # formatting title to some_title_name
    title = title.lower().replace(' ', '_')
        
    return os.path.join('graphic', 
                        title,
                        'chapters', 
                        instance.chapter.title,
                        filename)


def get_text_chapter_path(instance, filename):
    """Creates the path to the chapter of a text book"""
    # if there is no title in eng, use russian
    title = instance.chapter.book.title_eng
    if not title:
        title = instance.chapter.book.title_rus
    
    # formatting title to some_title_name
    title = title.lower().replace(' ', '_')

    return os.path.join('text', 
                        instance.chapter.book.title_eng,
                        'chapters', 
                        instance.chapter.title,
                        filename)


# Create your models here.
class Book(models.Model):
    """
    Represents a basic book model and its common attributes both
    for graphic and text content
    """
    title_rus = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()


class TextBook(Book):
    """A book with text only"""
    # for specification purposes
    pass


class GraphicBook(Book):
    """A comic book or manga only"""
    # for specification purposes
    pass


class TextBookChapter(models.Model):
    """Represents a chapter from a certain text book"""
    book = models.ForeignKey(
        TextBook, 
        on_delete=models.CASCADE,
        related_name='chapters'     # access book's chapters with .chapters.all()
        )
    title = models.CharField(max_length=255)
    # a file with the chapter's content
    text_content = models.FileField(
        upload_to=get_text_chapter_path,
        )
    class Meta:
        # chapters are ordered by their ids
        ordering = ["id"]


class GraphicBookChapter(models.Model):
    """Represents a chapter from a certain graphic book"""
    book = models.ForeignKey(
        GraphicBook, 
        on_delete=models.CASCADE,
        related_name='chapters'     # access book's chapters with obj.chapters.all()
        )
    title = models.CharField(max_length=255)

    class Meta:
        # chapters are ordered by their ids
        ordering = ["id"]


class GraphicBookPage(models.Model):
    """A page for a graphic book chapter"""
    chapter = models.ForeignKey(
        GraphicBookChapter, 
        on_delete=models.CASCADE,
        related_name='pages'        # access book's chapters with obj.pages.all()
        )
    image = models.ImageField(upload_to=get_graphic_chapter_path)
    page_number = models.PositiveIntegerField()

    class Meta:
        # we should sort by page number
        ordering = ['page_number']
        # one page №(some number) for a chapter
        unique_together = ['chapter', 'page_number']
