"""Views for 'main' app, pages with content"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from itertools import chain
from users.models import User
from . models import TextTitle, GraphicTitle
from . forms import TextTitleForm, GraphicTitleForm


# Create your views here.
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
    title = Title.objects.get(id=title_id)

    if title:
        context = {
            'title': title
        }
    else:
        context = {}
    return render(request, 'main/title_page.html', context)


@login_required
def upload_title(request):
    # there can be 'graphic' or 'text' content type
    title_type = request.GET.get('title_type')

    if request.method == 'POST':
        if title_type == 'graphic':
            form = GraphicTitleForm(request.POST)
        elif title_type == 'text':
            form = TextTitleForm(request.POST)
        else:
            pass # TODO: add response here
        if form.is_valid():
            form.save()
            return redirect('main:home')
    else:
        if title_type == 'graphic':
            form = GraphicTitleForm()
        elif title_type == 'text':
            form = TextTitleForm()
        else:
            pass # TODO: add response here
    print(title_type)
    context = {
        'form': form,
        'title_type': title_type
    }
    
    return render(request, 'main/upload_title.html', context)


def upload_chapter(request, title_id):
    pass

