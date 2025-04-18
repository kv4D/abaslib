"""Views for 'reader' app, manage reading process"""
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from titles.models import TextTitle, GraphicTitle, TextTitleChapter, \
    GraphicTitleChapter, GraphicTitlePage
from main.utils import redirect_to_title_page
from metadata.utils import update_views
from . models import TextTitleBookmark, GraphicTitleBookmark
from . utils import process_chapter_switch


def start_read_text_view(request, title_id):
    """Start reading from the start"""
    first_chapter = TextTitleChapter.objects.filter(
        title=get_object_or_404(TextTitle, id=title_id)
    ).first()
    
    if first_chapter is None:
        return redirect_to_title_page(title_id, 'text')
    
    response = redirect('reader:read_text', title_id=title_id)
    response['Location'] += f'?chapter_num={first_chapter.chapter_number}'
    return response


def start_read_graphic_view(request, title_id):
    """Start reading from the start"""
    first_chapter = GraphicTitleChapter.objects.filter(
        title=get_object_or_404(GraphicTitle, id=title_id)
    ).first()
    
    if first_chapter is None:
        return redirect_to_title_page(title_id, 'graphic')
    
    response = redirect('reader:read_graphic', title_id=title_id)
    response['Location'] += f'?chapter_num={first_chapter.chapter_number}&page=1'
    return response
    

def read_text_title_view(request, title_id):
    """Render page with chapter's content"""
    chapter_number = request.GET.get('chapter_num')
    chapter_number = float(str(chapter_number).replace(',', '.'))
    
    title = get_object_or_404(TextTitle, id=title_id)
    try:
        chapter = TextTitleChapter.objects.get(chapter_number=float(chapter_number), title=title)
    except Exception as e:
        # for some reason there is no chapter
        # back to title's page
        return redirect_to_title_page(title_id, 'text')

    # always remember about encodings
    with open(chapter.text_content.path, "r", encoding='utf-8') as file:
        chapter_content = file.read()

    # update views
    update_views(request, title)

    # for user selection
    all_chapters = title.text_chapters.all()

    context = {
        'title': title,
        'current_chapter': chapter,
        'chapter_content': chapter_content,
        'all_chapters': all_chapters
    }

    return render(request, 'reader/read_text.html', context)


def read_graphic_title_view(request, title_id):
    """Render page with one of the chapter's pages"""
    try:
        get_params = request.GET.copy()
        chapter_number = float(get_params.get('chapter_num', 1).replace(',', '.'))
        
        page_number = int(get_params.get('page', 1))
        title = get_object_or_404(GraphicTitle, id=title_id)
        chapter = GraphicTitleChapter.objects.get(chapter_number=chapter_number, title=title)

        page_number, chapter, get_params = process_chapter_switch(
            page_number,
            chapter, title,
            get_params
            )

        # parameters have changed, load another chapter
        if get_params != request.GET.copy():
            response = reverse('reader:read_graphic', args=[title_id])
            # new get parameters
            response += f"?{get_params.urlencode()}"
            return redirect(response)
    except Exception as e:
        # for some reason no chapters to load (empty or nonexistent)
        # return to the title page
        print(e)
        return redirect_to_title_page(title_id, 'graphic')

    page = chapter.pages.filter(page_number=page_number).first()

    # use urls
    page_image = page.image.url

    # update views
    update_views(request, title)

    # for user selection
    all_chapters = GraphicTitleChapter.objects.filter(title=title).all()
    all_pages = GraphicTitlePage.objects.filter(chapter=chapter).all()

    context = {
        'title': title,
        'current_chapter': chapter,
        'current_page': page,
        'page_image': page_image,
        'all_chapters': all_chapters,
        'all_pages': all_pages
    }

    return render(request, 'reader/read_graphic.html', context)


@login_required
def open_bookmark_view(request, title_id):
    """Start reading on the active bookmark"""
    user = request.user
    title_type = request.GET.get('title_type')

    if title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
    elif title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)



@login_required
def manage_bookmark_view(request, title_id, chapter_id):
    """Make a bookmark on this title's chapter"""
    user = request.user
    title_type = request.GET.get('title_type')

    assert title_type in ['text', 'graphic']

    if title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        chapter = get_object_or_404(TextTitleChapter, id=chapter_id)
        bookmark, is_created = TextTitleBookmark.objects.get_or_create(
            user=user,
            chapter=chapter,
            title=title
        )
    elif title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
        chapter = get_object_or_404(GraphicTitleChapter, id=chapter_id)
        bookmark, is_created = GraphicTitleBookmark.objects.get_or_create(
            user=user,
            chapter=chapter,
            title=title
        )
