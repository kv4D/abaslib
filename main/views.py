"""Views for 'main' app, pages with content"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from metadata.models import TitleView, TitleFavorite
from titles.models import TextTitle, GraphicTitle
from titles import utils


# create views here.
def home_view(request):
    """Renders website's home page"""

    context = {
        'new_titles': utils.get_new_titles(),
        'updated_titles': utils.get_updated_titles(),
        }

    return render(request, 'main/home.html', context)


def text_titles_view(request):
    """Renders page with text titles"""

    context = {
        'text_titles': TextTitle.get_titles()
    }

    return render(request, 'main/text_titles.html', context)


def graphic_titles_view(request):
    """Renders page with graphic titles"""

    context = {
        'graphic_titles': GraphicTitle.get_titles()
    }

    return render(request, 'main/graphic_titles.html', context)


def collect_about_section(request, title_type, title_id):
    """Creates context for about section of title's page"""
    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        
    # collect and update stats
    title.views_count = TitleView.get_views_count(title)
    title.favorites_count = TitleFavorite.get_favorite_count(title)
    title.save()
    is_favorite = utils.get_favorite_status(request.user, title)

    context = {
        'title': title,
        'title_type': title_type,
        'user_favorite': is_favorite
    }

    return context


def collect_chapters_section(request, title_type, title_id):
    """Creates context for chapters section of title's page"""
    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
        chapters = title.graphic_chapters.all()
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        chapters = title.text_chapters.all()

    is_favorite = utils.get_favorite_status(request.user, title)

    context = {
        'title': title,
        'chapters': chapters,
        'title_type': title_type,
        'user_favorite': is_favorite
    }

    return context


def collect_comment_section(request, title_type, title_id):
    """Creates context for comment section of title's page"""
    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)

    is_favorite = utils.get_favorite_status(request.user, title)

    if title:
        context = {
            'title': title,
            'title_type': title_type,
            'user_favorite': is_favorite
        }
    else:
        context = {}

    return context


def title_page_view(request, title_id=None):
    """Renders title page with specific context"""
    section = request.GET.get('section')
    title_type = request.GET.get('title_type')

    # collect context for different sections
    assert section in ['about', 'chapters', 'comments']

    if section == 'about':
        context = collect_about_section(request, title_type, title_id)
    elif section == 'chapters':
        context = collect_chapters_section(request, title_type, title_id)
    elif section == 'comments':
        context = collect_comment_section(request, title_type, title_id)

    return render(request, 'main/title_page.html', context)


@login_required
def change_favorite_title_status(request, title_id=None):
    """
    Changes 'favorite' status of title for users when they press the button
    on title page
    """
    title_type = request.GET.get('title_type')
    user = request.user

    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        
    content_type = ContentType.objects.get_for_model(title)
        
    if user.has_title_in_favorites(title):
        user.remove_title_from_favorites(title)
        TitleFavorite.objects.filter(
            user=user, 
            content_type=content_type,
            object_id=title_id).delete()
    else:
        user.add_title_to_favorites(title)
        TitleFavorite.objects.create(
            user = user,
            content_object = title
        )

    return utils.redirect_to_title_page(title_id, title_type, request.GET.get('section'))
