"""Views for 'main' app, pages with content"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from itertools import chain
from users.models import User
from . models import Title, TextTitle, GraphicTitle, GraphicTitlePage
from . forms import TextTitleForm, GraphicTitleForm, GraphicTitleChapterForm, TextTitleChapterForm, GraphicTitlePageFormSet


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

    context['titles'] = titles[:5]

    return render(request, 'main/home.html', context)


def title_page_view(request, title_id=None):
    """Renders title's page, provides title's info"""
    title_type = request.GET.get('title_type')
    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
    else:
        pass

    if title:
        context = {
            'title': title,
            'title_type': title_type
        }
    else:
        context = {}
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
def upload_chapter_view(request, title_id=None):
    # there can be 'graphic' or 'text' content type
    title_type = request.GET.get('title_type')
    
    if title_type == 'text':
        print(1)
        form = TextTitleChapterForm
        title = get_object_or_404(TextTitle, id=title_id)
    else:
        form = GraphicTitleChapterForm
        title = get_object_or_404(GraphicTitle, id=title_id)
        
    if request.method == 'POST':
        print(2)
        form = form(request.POST, request.FILES, title=title)
        if form.is_valid():
            print(3)
            chapter = form.save(commit=False)
            chapter.title = title
            chapter.save()
            
            if isinstance(title, GraphicTitle):
                images = request.FILES.getlist('image')
                for image in images:
                    GraphicTitlePage.objects.create(chapter=chapter, image=image)
            
            response = redirect('main:title_page', title_id=title_id)
            response['Location'] += f'?title_type={title_type}'
            return response
    else:
        form = form(title=title)

    context = {
        'form': form,
        'title': title,
        'title_type': title_type
    }
    
    return render(request, 'main/upload_chapter.html', context)
