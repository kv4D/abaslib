"""Views for 'main' app, pages with content"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from users.models import User
from . models import Title
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

    return render(request, 'main/home.html', context)


def title_page_view(request, title_id: int, title_name: str):
    """Renders title's page, provides title's info"""
    title = Title.objects.get(id=title_id, title_name_eng=title_name)

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
    if title_type == 'graphic':
        print('1')
        form = GraphicTitleForm()
    elif title_type == 'text':
        print('2')
        form = TextTitleForm()
    else:
        print('3')
        pass # add response here

    if request.method == 'POST':
        print('4')
        form.data = request.POST
        if form.is_valid():
            title = form.save()
            # TODO: create title and go for chapter creation or to title page
            return redirect('for later', title_id=title.id)

    context = {
        'form': form
    }
    
    return render(request, 'main/upload_title.html', context)


def upload_chapter(request, title_id):
    pass

