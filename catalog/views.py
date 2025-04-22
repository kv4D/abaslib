"""Views for 'catalog' app, pages with content"""
from itertools import chain
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from metadata.models import TitleView, TitleFavorite
from metadata.forms import FilterTagForm
from titles.models import TextTitle, GraphicTitle
from titles.utils import get_new_titles, get_updated_titles
from ratings.models import TitleRating
from . utils import redirect_to_title_page


# create views here.
def home_view(request):
    """Renders website's home page"""
    
    context = {
        'new_titles': get_new_titles(),
        'updated_titles': get_updated_titles()
        }
    return render(request, 'catalog/home.html', context)


def all_titles_view(request):
    """Renders page with all titles"""
    filter_form = FilterTagForm(request.GET)
    text_titles = TextTitle.objects.all()
    graphic_titles = GraphicTitle.objects.all()
    
    if filter_form.is_valid():
        genres = filter_form.cleaned_data.get('genres')
        tags = filter_form.cleaned_data.get('tags')
        
        if genres:
            text_titles = TextTitle.objects.filter(genres__tag_genre__in=genres).distinct()
            graphic_titles = GraphicTitle.objects.filter(genres__tag_genre__in=genres).distinct()
        if tags:
            text_titles = TextTitle.objects.filter(tags__tag__in=tags).distinct()
            graphic_titles = GraphicTitle.objects.filter(tags__tag__in=tags).distinct()
            
    titles = sorted(
        chain(text_titles, graphic_titles),
        key=lambda title: title.added_at,
        reverse=True
    )
            
    context = {
        'titles': titles,
        'filter_form': filter_form
    }
    return render(request, 'catalog/all_titles.html', context)


def text_titles_view(request):
    """Renders page with text titles"""
    filter_form = FilterTagForm(request.GET)
    text_titles = TextTitle.objects.all()
    
    if filter_form.is_valid():
        genres = filter_form.cleaned_data.get('genres')
        tags = filter_form.cleaned_data.get('tags')
        
        if genres:
            text_titles = TextTitle.objects.filter(genres__tag_genre__in=genres).distinct()
        if tags:
            text_titles = TextTitle.objects.filter(tags__tag__in=tags).distinct()
    
    context = {
        'text_titles': text_titles,
        'filter_form': filter_form
    }
    return render(request, 'catalog/text_titles.html', context)


def graphic_titles_view(request):
    """Renders page with graphic titles"""
    filter_form = FilterTagForm(request.GET)
    graphic_titles = GraphicTitle.objects.all()
    
    if filter_form.is_valid():
        genres = filter_form.cleaned_data.get('genres')
        tags = filter_form.cleaned_data.get('tags')
        
        if genres:
            graphic_titles = graphic_titles.filter(genres__tag_genre__in=genres).distinct()
        if tags:
            graphic_titles = graphic_titles.filter(tags__tag__in=tags).distinct()
            
    context = {
        'graphic_titles': graphic_titles,
        'filter_form': filter_form
    }
    return render(request, 'catalog/graphic_titles.html', context)


def collect_about_section(request, title_type, title_id):
    """Creates context for about section of title's page"""
    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        
    # collect and update stats
    
    # metadata
    title.views_count = TitleView.get_views_count(title)
    title.favorites_count = TitleFavorite.get_favorite_count(title)
    title.save()
    is_favorite = TitleFavorite.get_favorite_status(title, request.user)
    tags = [relation.tag for relation in title.tags.all()]
    genres = [relation.tag_genre for relation in title.genres.all()]
    
    # ratings
    average_rate = TitleRating.get_average_rate(title)
    if request.user.is_authenticated:
        user_rate = title.ratings.filter(user=request.user).first()
    else:
        user_rate = 0
    
    user_rate = user_rate.rate if user_rate else 0
    rates_count = TitleRating.get_rates_count(title)

    context = {
        'title': title,
        'title_type': title_type,
        'user_favorite': is_favorite,
        'tags': tags,
        'genres': genres,
        'average_rate': average_rate,
        'rates_count': rates_count,
        'user_rate': user_rate
    }

    return context, 'catalog/title_page_about.html'


def collect_chapters_section(request, title_type, title_id):
    """Creates context for chapters section of title's page"""
    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
        chapters = title.graphic_chapters.all()
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        chapters = title.text_chapters.all()

    is_favorite = TitleFavorite.get_favorite_status(title, request.user)

    context = {
        'title': title,
        'chapters': chapters,
        'title_type': title_type,
        'user_favorite': is_favorite
    }

    return context, 'catalog/title_page_chapters.html'


def collect_comment_section(request, title_type, title_id):
    """Creates context for comment section of title's page"""
    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)

    is_favorite = TitleFavorite.get_favorite_status(title, request.user)

    if title:
        context = {
            'title': title,
            'title_type': title_type,
            'user_favorite': is_favorite
        }
    else:
        context = {}

    return context, 'catalog/title_page_comments.html'


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


@login_required(login_url="users:login")
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
        
    if TitleFavorite.get_favorite_status(title, user):
        user.remove_title_from_favorites(title)
        TitleFavorite.objects.filter(
            user=user, 
            content_type=content_type,
            object_id=title_id).delete()
    else:
        user.add_title_to_favorites(title)
        TitleFavorite.objects.create(
            user=user,
            content_object=title,
        )

    return redirect_to_title_page(title_id, title_type, request.GET.get('section'))
