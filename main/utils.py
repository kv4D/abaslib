"""Functions for certain purposes within apps"""
from re import search
from django.shortcuts import redirect
from itertools import chain
from . models import GraphicTitlePage, TextTitle, GraphicTitle, \
    GraphicTitleChapter, TextTitleChapter
    

def get_text_titles(return_amount: int = None):
    """Get first 'return_amount' text titles"""
    text_titles = TextTitle.objects.all()[:return_amount]
    return text_titles


def get_graphic_titles(return_amount: int = None):
    """Get first 'return_amount' graphic titles"""
    text_titles = GraphicTitle.objects.all()[:return_amount]
    return text_titles


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


def redirect_to_title_page(title_id: int, title_type: str, section: str = 'about'):
    """Redirect to provided title's page"""
    response = redirect('main:title_page', title_id=title_id)
    response['Location'] += f'?title_type={ title_type }&section={section}'
    return response


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
        for image in images:
            match = search(r'(\d+)', image.name)
            page_number = int(match.group()) if match else 10_000

            GraphicTitlePage.objects.create(
                chapter = chapter,
                image=image,
                page_number=page_number
            )
            