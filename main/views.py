"""Views for 'main' app, pages with content"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from itertools import chain
from users.models import User
from . models import TextTitle, GraphicTitle
from . forms import TextTitleForm, GraphicTitleForm, GraphicTitleChapterForm, TextTitleChapterForm


def select_title_form(title_type, post_data=None):
    """Selects proper title form according to title's type"""
    if title_type == 'graphic':
        if postdata:
            return GraphicTitleForm(request.POST)
        return GraphicTitleForm()
    
    elif title_type == 'text':
        if postdata:
            return TextTitleForm(request.POST)
        return TextTitleForm()
    
    else:
        return # TODO: add response here
    

def select_chapter_form(title_type, title_id, post_data=None):
    """Selects proper chapter form according to title's type"""
    if title_type == 'graphic':
        title = GraphicTitle.objects.get(id=title_id)
        if post_data:
            form = GraphicTitleChapterForm(request.POST)
        else:
            form = GraphicTitleChapterForm()
        return form, title
            
    elif title_type == 'text':
        title = TextTitle.objects.get(id=title_id)
        if post_data:
            form = TextTitleChapterForm(request.POST)
        else:
            form = TextTitleChapterForm()
        return form, title
    
    else:
        return # TODO: add response here


# create views here.
def home_view(request):
    """Renders website's home page with optional user info"""
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
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

    context['titles'] = titles

    return render(request, 'main/home.html', context)


def title_page_view(request, title_id):
    """Renders title's page, provides title's info"""
    title_type = request.GET.get('title_type')
    if title_type == 'graphic':
        title = GraphicTitle.objects.get(id=title_id)
    elif title_type == 'text':
        title = TextTitle.objects.get(id=title_id)
    else:
        pass # TODO: add response here

    if title:
        context = {
            'title': title
        }
    else:
        context = {}
    return render(request, 'main/title_page.html', context)


@login_required
def upload_title_view(request):
    # there can be 'graphic' or 'text' content type
    title_type = request.GET.get('title_type')

    if request.method == 'POST':
        form = select_title_form(title_type, request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:home')
    else:
        form = select_title_form(title_type)
        
    context = {
        'form': form,
        'title_type': title_type
    }
    
    return render(request, 'main/upload_title.html', context)


def upload_chapter_view(request, title_id):
    # there can be 'graphic' or 'text' content type
    title_type = request.GET.get('title_type')

    if request.method == 'POST':
        form, title = select_chapter_form(title_type, title_id, request.POST)
        if form.is_valid():
            form.save()
            return redirect('main/title_page.html')
    else:
        form, title = select_chapter_form(title_type, title_id)

    context = {
        'form': form,
        'title': title,
        'title_type': title_type
    }
    
    return render(request, 'main/upload_chapter.html', context)

