import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone


def get_graphic_chapter_path(instance, filename):
    """Creates the path to the chapter of a graphic title"""
    title_id = instance.chapter.title.id
    return os.path.join(
        'graphic', str(title_id), 'chapters', instance.chapter.chapter_name, filename
        )


def get_graphic_title_cover_path(instance, filename):
    """Creates the path to title's cover"""
    title_id = instance.id
    return os.path.join(
        'covers', 'graphic', str(title_id), filename
        )


def get_text_chapter_path(instance, filename):
    """Creates the path to the chapter of a text title"""
    title_id = instance.title.id
    return os.path.join(
        'text', str(title_id), 'chapters', instance.chapter_name, filename
        )


def get_text_title_cover_path(instance, filename):
    """Creates the path to title's cover"""
    title_id = instance.id
    return os.path.join(
        'covers', 'text', str(title_id), filename
        )


class Title(models.Model):
    """
    Represents a basic title model and its common attributes both
    for graphic and text content
    """
    title_name_rus = models.CharField(max_length=100,
                                      unique=True,
                                      verbose_name=_('Название тайтла'))
    title_name_eng = models.CharField(max_length=100,
                                      unique=True,
                                      blank=True,
                                      verbose_name=_('Название тайтла (английское)'))
    title_author = models.CharField(max_length=100,
                                    verbose_name=_('Автор'))
    title_is_ongoing = models.BooleanField(default=True,
                                           verbose_name=_('Статус (продолжается - галочка, закончено - пусто)'))
    title_description = models.TextField(verbose_name=_('Описание'))
    publication_year = models.PositiveSmallIntegerField(default=timezone.now().year,
                                                        verbose_name=_('Год выпуска'))
    added_at = models.DateTimeField(auto_now_add=True,
                                    verbose_name=_('Добавлено'))

    views_count = models.PositiveIntegerField(default=0,
                                              verbose_name=_('Количество просмотров'))
    views = GenericRelation('metadata.TitleView')

    favorites_count = models.PositiveIntegerField(default=0,
                                                  verbose_name=_('Количество людей, добавивших в избранное'))
    favorites = GenericRelation('metadata.TitleFavorite')
    
    tags = GenericRelation('metadata.TitleTag')
    genres = GenericRelation('metadata.TitleGenre')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title_name_rus} ({self.title_name_eng})'


class TextTitle(Title):
    """A title with text only"""
    # for specification purposes
    title_cover = models.ImageField(
        default='default_cover.jpg',
        upload_to=get_text_title_cover_path,
        verbose_name=_('Обложка')
        )

    class Meta:
        verbose_name = _('Новелла')
        verbose_name_plural = _('Новеллы')
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

    @staticmethod
    def get_titles(return_amount = None):
        """Get first 'return_amount' text titles"""
        # from new to old
        return TextTitle.objects.all()[:return_amount:-1]


class GraphicTitle(Title):
    """A comic title or manga only"""
    # for specification purposes
    title_cover = models.ImageField(
        default='default_cover.jpg',
        upload_to=get_graphic_title_cover_path,
        verbose_name=_('Обложка')
        )

    class Meta:
        verbose_name = _('Комикс')
        verbose_name_plural = _('Комиксы')
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

    @staticmethod
    def get_titles(return_amount = None):
        """Get first 'return_amount' graphic titles"""
        # from new to old
        return GraphicTitle.objects.all()[:return_amount:-1]


class TitleChapter(models.Model):
    """
    Represents a basic title chapter model and its common attributes both
    for graphic and text content
    """
    chapter_name = models.CharField(max_length=255,
                                    blank=True,
                                    verbose_name=_('Название'))
    # because there is sometimes chapters with letters
    # example: chapter 0A or chapter 4K
    display_number = models.CharField(max_length=20,
                                      blank=True,
                                      verbose_name=_('Номер главы для отображения'))
    # because there is sometime extra chapters
    # example: chapter 5.5 (extra to 5th chapter)
    chapter_number = models.DecimalField(max_digits=5,
                                         decimal_places=1,
                                         verbose_name=_('Фактический номер главы'))
    # there is only one volume often
    volume = models.PositiveIntegerField(default=1,
                                         verbose_name=_('Том главы'))
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['chapter_number']
        # chapters are ordered by their ids
        constraints = [
            models.CheckConstraint(check=models.Q(chapter_number__gte=0), name="chapter_number_not_negative"),
        ]

    def __str__(self):
        if self.chapter_name:
            return f'Глава {self.display_number}: {self.chapter_name}'
        return f'Глава {self.display_number}'


class TextTitleChapter(TitleChapter):
    """Represents a chapter from a certain text title"""
    # a file with the chapter's content
    title = models.ForeignKey(
        TextTitle,
        on_delete=models.CASCADE,
        related_name='text_chapters',
        verbose_name=_('Связанный тайтл')
        )
    text_content = models.FileField(upload_to=get_text_chapter_path,
                                    verbose_name=_('Содержимое главы'))

    class Meta:
        verbose_name = _('Глава новеллы')
        verbose_name_plural = _('Главы новелл')
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


class GraphicTitleChapter(TitleChapter):
    """Represents a chapter from a certain graphic title"""
    # for specification purposes
    title = models.ForeignKey(
        GraphicTitle,
        on_delete=models.CASCADE,
        related_name='graphic_chapters',
        verbose_name=_('Связанный тайтл')
        )

    class Meta:
        verbose_name = _('Глава комикса')
        verbose_name_plural = _('Главы комиксов')
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


class GraphicTitlePage(models.Model):
    """A page for a graphic title chapter"""
    # access chapters's pages with obj.pages.all()
    chapter = models.ForeignKey(
        GraphicTitleChapter,
        on_delete=models.CASCADE,
        related_name='pages',
        verbose_name=_('Связанная глава')
        )
    image = models.ImageField(upload_to=get_graphic_chapter_path,
                              verbose_name=_('Страница (изображение)'))
    page_number = models.PositiveIntegerField(verbose_name=_('Номер страницы'))

    class Meta:
        verbose_name = _('Страница комикса')
        verbose_name_plural = _('Страницы комиксов')
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
