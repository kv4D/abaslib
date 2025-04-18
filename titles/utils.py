"""Functions for certain purposes within apps"""
from re import search
from django.db import transaction
from django.db.models import Max
from itertools import chain
from titles.models import GraphicTitlePage, TextTitle, GraphicTitle, \
    GraphicTitleChapter, TextTitleChapter


def get_new_titles(return_amount: int = 5):
    """Get first 'return_amount' titles of all new titles"""
    text_titles = TextTitle.objects.all()[:return_amount]
    graphic_titles = GraphicTitle.objects.all()[:return_amount]

    # unite titles and sort by date added
    titles = sorted(
        chain(text_titles, graphic_titles),
        key=lambda title: title.added_at,
        reverse=True
    )

    return titles[:return_amount]


def get_updated_titles(return_amount: int = 5):
    """Get first 'return_amount' recently updated titles"""
    text_chapters = TextTitleChapter.objects.all()
    graphic_chapters = GraphicTitleChapter.objects.all()

    # unite chapters and sort by chapter date added
    chapters = sorted(
        chain(text_chapters, graphic_chapters),
        key=lambda chapter: chapter.added_at,
        reverse=True
    )

    titles = []
    for chapter in chapters:
        if len(titles) == return_amount:
            break
        if chapter.title not in titles:
            titles.append(chapter.title)

    return titles[:return_amount]


def get_last_title_chapter(title):
    """Get title's chapter with the greatest chapter number"""
    if title.title_type == 'graphic':
        chapter_number = title.graphic_chapters.aggregate(
            Max('chapter_number')
            )['chapter_number__max']
        return chapter_number if chapter_number else 0
    elif title.title_type == 'text':
        chapter_number = title.text_chapters.aggregate(
            Max('chapter_number')
            )['chapter_number__max']
        return chapter_number if chapter_number else 0


def create_pages_from_list(images, chapter):
    """Create GraphicTitlePage objects with provided data"""
    if len(images) == 1:
        # only one page on chapter
        GraphicTitlePage.objects.create(
            chapter = chapter,
            image=images[0],
            page_number=1
        )
    else:
        # assume that pages have numeration already
        page_numbers = []
        for image in images:
            match = search(r'(\d+)', image.name)
            if match:
                page_numbers.append(int(match.group()))
        
        if page_numbers and len(page_numbers) == len(images):
            # there is some numeration
            # create order 
            sorted_images = sorted(images, 
                            key=lambda image: int(search(r'(\d+)', image.name).group(1)))
            
            with transaction.atomic():
                GraphicTitlePage.objects.bulk_create([
                    GraphicTitlePage(
                        chapter=chapter,
                        image=image,
                        page_number=number + 1
                    )
                    for number, image in enumerate(sorted_images)
                ])
        else:
            # there is no proper numeration
            # use upload order
            with transaction.atomic():
                GraphicTitlePage.objects.bulk_create([
                    GraphicTitlePage(
                        chapter=chapter,
                        image=image,
                        page_number=number+1
                    )
                    for number, image in enumerate(images)
                ])
