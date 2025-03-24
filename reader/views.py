from django.shortcuts import render, get_object_or_404, redirect
from django.http import QueryDict
from main.models import TextTitle, GraphicTitle, TextTitleChapter, GraphicTitleChapter, GraphicTitlePage


# TODO: manage impossible pages (last pages + first pages)
# Create your views here.
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
    if page_number > chapter.get_pages_amount():
        chapter = title.get_next_chapter(chapter)
        # start with the first page
        page_number = 1
        # change get parameters
        return page_number, chapter
    # try to get the previous chapter
    elif page_number < chapter.get_pages_amount():
        chapter = title.get_previous_chapter(chapter)
        # start with the last page
        page_number = chapter.pages.count()
        # change get parameters
        return page_number, chapter, get_params
    # no switch required
    return page_number, chapter, get_params


def read_graphic_title_view(request, title_id):
    """Render page with one of the chapter's pages"""
    get_params = request.GET.copy()
    chapter_number = get_params['chapter_num']
    page_number = get_params['page']

    title = get_object_or_404(GraphicTitle, id=title_id)
    chapter = GraphicTitleChapter.objects.get(chapter_number=chapter_number, title=title)

    #page_number, chapter = process_chapter_switch(page_number, chapter, title, get_params)

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
