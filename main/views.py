"""Views for 'main' app, pages with content"""
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required, permission_required
from itertools import chain
from users.models import User
from . models import TextTitle, GraphicTitle, GraphicTitlePage, \
    GraphicTitleChapter, TextTitleChapter
from . forms import TextTitleForm, GraphicTitleForm, \
    GraphicTitleChapterForm, TextTitleChapterForm, GraphicTitlePageForm


# create views here.
def home_view(request):
    """Renders website's home page with optional user info"""
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        context = {
            'user': user
        }
    else:
        context = {}
    
    text_titles = TextTitle.objects.all()
    graphic_titles = GraphicTitle.objects.all()

    # unite titles and sort by date added
    titles = sorted(
        chain(text_titles, graphic_titles), 
        key=lambda title: title.added_at,
        reverse=True
    )

    context['titles'] = titles[:10]

    return render(request, 'main/home.html', context)


def about_rights_view(request):
    return render(request, 'main/about_rights.html')


def render_about_section(title_type, title_id):
    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
    else:
        pass

    if title:
        context = {
            'title': title,
            'title_type': title_type,
            'section': 'about'
        }
    else:
        context = {}
        
    return context


def render_chapter_section(title_type, title_id):
    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
        chapters = title.graphic_chapters.all()
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        chapters = title.text_chapters.all()
    else:
        pass

    if title:
        context = {
            'title': title,
            'chapters': chapters,
            'title_type': title_type,
            'section': 'chapters'
        }
    else:
        context = {}
        
    return context


def render_comment_section(title_type, title_id):
    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
    else:
        pass
    
    if title:
        context = {
            'title': title,
            'title_type': title_type,
            'section': 'comments'
        }
    else:
        context = {}
        
    return context


def title_page_view(request, title_id=None):
    """Decides which section of title page to load"""
    section = request.GET.get('section')
    title_type = request.GET.get('title_type')
    
    if section == 'about':
        context = render_about_section(title_type, title_id)
    elif section == 'chapters':
        context = render_chapter_section(title_type, title_id)
    elif section == 'comments':
        context = render_comment_section(title_type, title_id)
    else:
        pass # TODO: add response here
    
    return render(request, 'main/title_page.html', context)    
    

@login_required
def upload_title_view(request):
    # there can be 'graphic' or 'text' content type
    title_type = request.GET.get('title_type')

    if title_type == 'text':
        form = TextTitleForm
    else:
        form = GraphicTitleForm

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:home')
    else:
        form = form()
        
    context = {
        'form': form,
        'title_type': title_type
    }
    
    return render(request, 'main/upload_title.html', context)


@login_required
def upload_text_chapter(request, title_id):
    title = get_object_or_404(GraphicTitle, id=title_id)
    
    if request.method == 'POST':
        form = TextTitleChapterForm(request.POST, title=title)
        if form.is_valid():
            form.save()
            
            response = redirect('main:title_page', title_id=title_id)
            response['Location'] += f'?title_type=text'
            return response
    else:
        form = TextTitleChapterForm(title=title)
        
    context = {
        'form': form,
        'title': title,
        'title_type': 'text'
    }
    
    return render(request, 'main/upload_chapter.html', context)
            

@login_required
def upload_graphic_chapter(request, title_id):
    title = get_object_or_404(GraphicTitle, id=title_id)
    
    if request.method == 'POST':
        form = GraphicTitleChapterForm(request.POST, title=title)
        if form.is_valid():
            form.save()
            
            response = redirect('main:title_page', title_id=title_id)
            response['Location'] += f'?title_type=graphic'
            return response
    else:
        form = GraphicTitleChapterForm(title=title)
        
    context = {
        'form': form,
        'title': title,
        'title_type': 'text'
    }
    
    return render(request, 'main/upload_chapter.html', context)


@login_required
def upload_chapter_view(request, title_id=None):
    # there can be 'graphic' or 'text' content type
    title_type = request.GET.get('title_type')
    
    if title_type == 'text':
        response = upload_text_chapter(request, title_id)
    else:
        response = upload_graphic_chapter(request, title_id)

    return response
