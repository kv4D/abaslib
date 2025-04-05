"""Views for 'main' app, pages with content"""
from re import search
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from reader import models
from . models import TextTitle, GraphicTitle
from . forms import TextTitleForm, GraphicTitleForm, \
    GraphicTitleChapterForm, TextTitleChapterForm, GraphicTitlePagesForm
from . utils import create_pages_from_list, get_new_titles, \
    redirect_to_title_page, get_updated_titles, get_graphic_titles, \
        get_text_titles


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
        'text_titles': get_text_titles()
    }
    
    return render(request, 'main/text_titles.html', context)


def graphic_titles_view(request):
    """Renders page with graphic titles"""
    
    context = {
        'graphic_titles': get_graphic_titles()
    }
    
    return render(request, 'main/graphic_titles.html', context)


def collect_about_section(request, title_type, title_id):
    """Creates context for about section of title's page"""
    assert title_type in ['text', 'graphic']
    
    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
    
    try:
        is_favorite = request.user.has_title_in_favorites(title)
    except AttributeError:
        # user is unauthorized
        is_favorite = None
    
    if title:
        context = {
            'title': title,
            'title_type': title_type,
            'user_favorite': is_favorite
        }
    else:
        context = {}

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
    else:
        pass

    try:
        is_favorite = request.user.has_title_in_favorites(title)
    except AttributeError:
        # user is unauthorized
        is_favorite = None
        
    if title:
        context = {
            'title': title,
            'chapters': chapters,
            'title_type': title_type,
            'user_favorite': is_favorite
        }
    else:
        context = {}

    return context


def collect_comment_section(request, title_type, title_id):
    """Creates context for comment section of title's page"""
    assert title_type in ['text', 'graphic']
    
    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
    
    try:
        is_favorite = request.user.has_title_in_favorites(title)
    except AttributeError:
        # user is unauthorized
        is_favorite = None
    
    if title:
        print(title.title_cover.url)
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
    
    assert title_type in ['text', 'graphic']
    
    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
        if request.user.has_title_in_favorites(title):
            request.user.remove_title_from_favorites(title)
            models.GraphicTitleFavorite.objects.filter(user=request.user, title=title).delete()
        else:
            request.user.add_title_to_favorites(title)
            models.GraphicTitleFavorite.objects.create(
                user = request.user,
                title = title
            )
        title.favorites_count = models.GraphicTitleFavorite.get_favorite_count(title)
        title.save()
            
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        if request.user.has_title_in_favorites(title):
            request.user.remove_title_from_favorites(title)
            models.TextTitleFavorite.objects.filter(user=request.user, title=title).delete()
        else:
            request.user.add_title_to_favorites(title)
            models.TextTitleFavorite.objects.create(
                user = request.user,
                title = title
            )
        title.favorites_count = models.TextTitleFavorite.get_favorite_count(title)
        title.save()


        
    return redirect_to_title_page(title_id, title_type, request.GET.get('section'))


@login_required
def upload_title_view(request):
    """Uploads title with provided info"""
    # there can be 'graphic' or 'text' content type
    title_type = request.GET.get('title_type')

    assert title_type in ['text', 'graphic']
    
    if title_type == 'text':
        form = TextTitleForm
    elif title_type == 'graphic':
        form = GraphicTitleForm

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:home')
    else:
        form = form()

    context = {
        'form': form
    }

    return render(request, 'main/upload_title.html', context)


@login_required
def upload_text_chapter(request, title_id):
    """Uploads text chapter with provided data"""
    title = get_object_or_404(TextTitle, id=title_id)

    if request.method == 'POST':
        form = TextTitleChapterForm(request.POST, request.FILES, title=title)
        if form.is_valid():
            form.save()
            return redirect_to_title_page(title_id, 'text')
    else:
        form = TextTitleChapterForm(title=title)

    context = {
        'form': form,
        'title': title
    }

    return render(request, 'main/upload_chapter.html', context)


@login_required
def upload_graphic_chapter(request, title_id):
    """Uploads graphic chapter with provided data"""
    title = get_object_or_404(GraphicTitle, id=title_id)

    if request.method == 'POST':
        chapter_form = GraphicTitleChapterForm(request.POST, title=title)
        pages_form = GraphicTitlePagesForm(request.POST, request.FILES)

        if chapter_form.is_valid() and pages_form.is_valid():
            chapter = chapter_form.save(commit=False)
            chapter.title = title
            chapter.save()

            # collect all of the images for pages
            images = request.FILES.getlist('images')
            create_pages_from_list(images, chapter)
            return redirect_to_title_page(title_id, 'graphic')
    else:
        chapter_form = GraphicTitleChapterForm(title=title)
        pages_form = GraphicTitlePagesForm()

    context = {
        'chapter_form': chapter_form,
        'pages_form': pages_form,
        'title': title
    }

    return render(request, 'main/upload_chapter.html', context)


@login_required
def upload_chapter_view(request, title_id=None):
    """Selects which title type to upload and provide response"""
    title_type = request.GET.get('title_type')

    assert title_type in ['text', 'graphic']
    
    if title_type == 'text':
        response = upload_text_chapter(request, title_id)
    elif title_type == 'graphic':
        response = upload_graphic_chapter(request, title_id)

    return response
