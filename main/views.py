"""Views for 'main' app, pages with content"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from metadata.models import TitleView, TitleFavorite, TitleGenre, TitleTag
from titles.models import TextTitle, GraphicTitle
from titles.utils import get_new_titles, get_updated_titles
from . utils import redirect_to_title_page


# create views here.
def home_view(request):
    """Renders website's home page"""
    context = {
        'new_titles': get_new_titles(),
        'updated_titles': get_updated_titles(),
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
    
    is_favorite = TitleFavorite.get_favorite_status(request.user, title)
    
    tags = TitleTag.get_all_title_tags(title)
    tags = [relation.tag for relation in tags]
    
    genres = TitleGenre.get_all_title_genres(title)
    genres = [relation.tag_genre for relation in genres]

    context = {
        'title': title,
        'title_type': title_type,
        'user_favorite': is_favorite,
        'tags': tags,
        'genres': genres
    }

    return context, 'main/title_page_about.html'


def collect_chapters_section(request, title_type, title_id):
    """Creates context for chapters section of title's page"""
    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
        chapters = title.graphic_chapters.all()
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        chapters = title.text_chapters.all()

    is_favorite = TitleFavorite.get_favorite_status(request.user, title)

    context = {
        'title': title,
        'chapters': chapters,
        'title_type': title_type,
        'user_favorite': is_favorite
    }

    return context, 'main/title_page_chapters.html'


def collect_comment_section(request, title_type, title_id):
    """Creates context for comment section of title's page"""
    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)

    is_favorite = TitleFavorite.get_favorite_status(request.user, title)

    if title:
        context = {
            'title': title,
            'title_type': title_type,
            'user_favorite': is_favorite
        }
    else:
        context = {}

    return context, 'main/title_page_comments.html'


def title_page_view(request, title_id=None):
    """Renders title page with specific context"""
    section = request.GET.get('section')
    title_type = request.GET.get('title_type')

    # collect context for different sections
    assert section in ['about', 'chapters', 'comments']

    if section == 'about':
        context, template = collect_about_section(request, title_type, title_id)
    elif section == 'chapters':
        context, template = collect_chapters_section(request, title_type, title_id)
    elif section == 'comments':
        context, template = collect_comment_section(request, title_type, title_id)

    return render(request, template, context)


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
            user=user,
            content_object=title
        )

    return redirect_to_title_page(title_id, title_type, request.GET.get('section'))
