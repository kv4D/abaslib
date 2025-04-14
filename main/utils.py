"""Functions for certain purposes within apps"""
from django.shortcuts import redirect


def redirect_to_title_page(title_id: int, title_type: str, section: str = 'about'):
    """Redirect to provided title's page"""
    response = redirect('main:title_page', title_id=title_id)
    response['Location'] += f'?title_type={ title_type }&section={section}'
    return response