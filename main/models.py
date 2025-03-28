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
    
    def get_next_chapter(self, chapter):
        """Tries to get the next chapter for the provided chapter"""
        if chapter.title != self:
            raise ValueError('Chapter does not belong to this book')
        chapter = self.text_chapters.filter(chapter_number__gt=chapter.chapter_number).first()
        if chapter is None:
            raise ValueError('No more chapters: it is the last chapter')
        return chapter
    
    def get_previous_chapter(self, chapter):
        """Tries to get the previous chapter for the provided chapter"""
        if chapter.title != self:
            raise ValueError('Chapter does not belong to this book')
        chapter = self.text_chapters.filter(chapter_number__lt=chapter.chapter_number).first()
        if chapter is None:
            raise ValueError('No more chapters: it is the first chapter')
        return chapter
        
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
    
    def get_next_chapter(self, chapter):        
        """Tries to get the next chapter for the provided chapter"""
        if chapter.title != self:
            raise ValueError('Chapter does not belong to this book')
        chapter =  self.graphic_chapters.filter(chapter_number__gt=chapter.chapter_number).first()
        if chapter is None:
            raise ValueError('No more chapters: it is the last chapter')
        if chapter.is_empty():
            raise ValueError('This chapter is empty')
        return chapter
        
    def get_previous_chapter(self, chapter):
        """Tries to get the previous chapter for the provided chapter"""
        if chapter.title != self:
            raise ValueError('Chapter does not belong to this book')
        chapter = self.graphic_chapters.filter(chapter_number__lt=chapter.chapter_number).last()

        if chapter is None:
            raise ValueError('No more chapters: it is the first chapter')        
        if chapter.is_empty():
            raise ValueError('This chapter is empty')
        return chapter
    
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
    chapter_name = models.CharField(max_length=255, blank=True)
    chapter_number = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        # chapters are ordered by their ids
        ordering = ["chapter_number"]


class TextTitleChapter(TitleChapter):
    """Represents a chapter from a certain text title"""
    # a file with the chapter's content
    title = models.ForeignKey(
        TextTitle,
        on_delete=models.CASCADE,
        related_name='text_chapters'
        )
    text_content = models.FileField(upload_to=get_text_chapter_path)
    
    class Meta:
        # one chapter for a title
        constraints = [
                models.UniqueConstraint(
                    fields=['title', 'chapter_number'],
                    name='unique_chapter_number_per_text_title'
                )
            ]

    def get_path(self):
        """Returns path to chapter"""
        return os.path.join('media', 'text', str(self.title.id), str(self.id))

    def is_empty(self):
        """Checks if chapter is empty (has no text_content)"""
        return self.text_content is None
    
    @property
    def title_type(self):
        """Returns title type"""
        return 'text'

    def __str__(self):
        if self.chapter_name:
            return f'Глава {self.chapter_number}: {self.chapter_name}'
        return f'Глава {self.chapter_number}'

class GraphicTitleChapter(TitleChapter):
    """Represents a chapter from a certain graphic title"""
    # for specification purposes
    title = models.ForeignKey(
        GraphicTitle,
        on_delete=models.CASCADE,
        related_name='graphic_chapters'
        )

    class Meta:
        # one chapter for a title
        constraints = [
                models.UniqueConstraint(
                    fields=['title', 'chapter_number'],
                    name='unique_chapter_number_per_graphic_title'
                )
            ]

    def get_path(self):
        """Returns path to chapter"""
        return os.path.join('media', 'graphic', str(self.title.id), str(self.id))
    
    def get_next_page(self, page):
        """Tries to get the next page for the provided page"""
        if page.chapter != self:
            raise ValueError('Page does not belong to this chapter')
        page = self.pages.filter(page_number__gt=page.page_number).first()
        if page is None:
            raise ValueError('No more pages: it is the last page')
        return page
    
    def get_previous_page(self, page):
        """Tries to get the previous page for the provided page"""
        if page.chapter != self:
            raise ValueError('Page does not belong to this chapter')
        page = self.pages.filter(page_number__lt=page.page_number).first()
        if page is None:
            raise ValueError('No more pages: it is the first page')
        return page
    
    def is_empty(self):
        """Checks if chapter is empty (has no pages)"""
        return self.pages.count() == 0
    
    @property
    def title_type(self):
        """Returns title type"""
        return 'graphic'
    
    def __str__(self):
        if self.chapter_name:
            return f'Глава {self.chapter_number}: {self.chapter_name}'
        return f'Глава {self.chapter_number}'


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
