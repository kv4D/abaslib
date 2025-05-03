from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import TextTitle, GraphicTitle
from . forms import TextTitleForm, GraphicTitleForm, \
                    TextTitleChapterForm, GraphicTitleChapterForm, \
                    GraphicTitlePagesForm, ChapterSelectForm
from . utils import create_pages_from_list, get_last_title_chapter
from catalog.utils import redirect_to_title_page


@login_required
def update_title_view(request, title_id):
    """Update title's fields with provided info"""
    title_type = request.GET.get('title_type')

    assert title_type in ['text', 'graphic']

    if title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        form = TextTitleForm
    elif title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
        form = GraphicTitleForm

    if request.method == 'POST':
        form = form(request.POST, request.FILES, instance=title)
        if form.is_valid():
            form.save()
            return redirect_to_title_page(title_id, title.title_type)
    else:
        form = form(instance=title)

    context = {
        'form': form,
        'title': title
    }

    return render(request, 'titles/update_title.html', context)


@login_required
def delete_chapter_view(request, title_id):
    """Deletes one certain chapter"""
    title_type = request.GET.get('title_type')

    assert title_type in ['text', 'graphic']

    if title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        chapters = title.text_chapters.all()
    elif title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
        chapters = title.graphic_chapters.all()
    
    if request.method == 'POST':
        chapter_id = request.POST.get('chapter')
        chapters.filter(id=chapter_id).delete()
        return redirect_to_title_page(title_id, title.title_type)
    
    form = ChapterSelectForm(title=title)
    
    context = {
        'title': title,
        'chapters': chapters, 
        'form': form
    }

    return render(request, 'titles/delete_chapter.html', context)
    
@login_required
def delete_title_view(request, title_id):
    """Deletes one certain title"""


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
        form = form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = form()

    context = {
        'form': form
    }

    return render(request, 'titles/upload_title.html', context)


@login_required
def upload_text_chapter(request, title_id):
    """Uploads text chapter with provided data"""
    title = get_object_or_404(TextTitle, id=title_id)

    if request.method == 'POST':
        form = TextTitleChapterForm(request.POST,
                                    request.FILES,
                                    title=title)
        if form.is_valid():
            form.save()
            return redirect_to_title_page(title_id, 'text')
    else:
        chapter_number = get_last_title_chapter(title) + 1
        form = TextTitleChapterForm(title=title,
                                    chapter_number=chapter_number)

    context = {
        'form': form,
        'title': title
    }

    return render(request, 'titles/upload_chapter.html', context)


@login_required
def upload_graphic_chapter(request, title_id):
    """Uploads graphic chapter with provided data"""
    title = get_object_or_404(GraphicTitle, id=title_id)

    if request.method == 'POST':
        chapter_form = GraphicTitleChapterForm(request.POST,
                                               title=title)
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
        chapter_number = get_last_title_chapter(title) + 1
        chapter_form = GraphicTitleChapterForm(title=title,
                                               chapter_number=chapter_number)
        pages_form = GraphicTitlePagesForm()

    context = {
        'chapter_form': chapter_form,
        'pages_form': pages_form,
        'title': title
    }

    return render(request, 'titles/upload_chapter.html', context)


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
