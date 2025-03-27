"""Functions for certain purposes"""
from re import search
from django.shortcuts import redirect
from itertools import chain
from . models import GraphicTitlePage, TextTitle, GraphicTitle


def get_new_titles(return_amount: int = 5):
    """Get first 'return_amount' titles of all new titles"""
    text_titles = TextTitle.objects.all()
    graphic_titles = GraphicTitle.objects.all()
    
    # unite titles and sort by date added
    titles = sorted(
        chain(text_titles, graphic_titles),
        key=lambda title: title.added_at,
        reverse=True
    )
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
            