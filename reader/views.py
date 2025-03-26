from django.shortcuts import render, get_object_or_404, redirect
from django.http import QueryDict
from django.urls import reverse
from main.models import TextTitle, GraphicTitle, TextTitleChapter, GraphicTitleChapter, GraphicTitlePage


def read_text_title_view(request, title_id):
    """Render page with chapter's content"""
    chapter_number = request.GET.get('chapter_num')

    title = get_object_or_404(TextTitle, id=title_id)
    chapter = TextTitleChapter.objects.get(chapter_number=chapter_number, title=title)

    # always remember about encodings
    with open(chapter.text_content.path, "r", encoding='utf-8') as file:
        chapter_content = file.read()

    # for user selection
    all_chapters = title.text_chapters.all()

    print(chapter)

    context = {
        'title': title,
        'current_chapter': chapter,
        'chapter_content': chapter_content,
        'all_chapters': all_chapters
    }

    return render(request, 'reader/read_text.html', context)


def process_chapter_switch(page_number,
                           chapter: GraphicTitleChapter,
                           title: GraphicTitle,
                           get_params: QueryDict):
    """Process page number and switches for other chapters"""
    # try to get the next chapter
    if page_number > chapter.pages.count():
        chapter = title.get_next_chapter(chapter)
        page_number = 1
        # modify get parameters
        get_params['page'] = str(page_number)
        get_params['chapter_num'] = str(chapter.chapter_number)
        return page_number, chapter, get_params
    # try to get the previous chapter
    elif page_number <= 0:
        chapter = title.get_previous_chapter(chapter)
        page_number = chapter.pages.count()
        # modify get parameters
        get_params['page'] = str(page_number)
        get_params['chapter_num'] = str(chapter.chapter_number)
        return page_number, chapter, get_params
    # no switch or modifications required
    return page_number, chapter, get_params


def read_graphic_title_view(request, title_id):
    """Render page with one of the chapter's pages"""
    get_params = request.GET.copy()
    
    chapter_number = int(get_params.get('chapter_num', 1))
    page_number = int(get_params.get('page', 1))

    title = get_object_or_404(GraphicTitle, id=title_id)
    chapter = GraphicTitleChapter.objects.get(chapter_number=chapter_number, title=title)

    try:
        page_number, chapter, get_params = process_chapter_switch(page_number, chapter, title, get_params)
        if get_params != request.GET.copy():
            response = reverse('reader:read_graphic', args=[title_id]) + f"?{get_params.urlencode()}"
            return redirect(response)
    except ValueError as e:
        # for some reason no chapters to load (empty or nonexistent)
        # return to the title page
        response = redirect('main:title_page', title_id=title_id)
        response['Location'] += '?title_type=graphic&section=about'
        return response

    page = chapter.pages.filter(page_number=page_number).first()

    # use urls
    page_image = page.image.url

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


def open_bookmark_view(request, title_id):
    """Start reading on the active bookmark"""
    pass