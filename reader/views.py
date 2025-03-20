from django.shortcuts import render, get_object_or_404
from main.models import TextTitle, GraphicTitle, TextTitleChapter, GraphicTitleChapter, GraphicTitlePage

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
    chapters_amount = TextTitleChapter.objects.filter(title=title).count()
    
    context = {
        'title': title,
        'current_chapter': chapter,
        'chapter_content': chapter_content,
        'chapters_amount': chapters_amount
    }
    
    return render(request, 'reader/read_text.html', context)


def read_graphic_title_view(request, title_id):
    """Render page with one of the chapter's pages"""
    chapter_number = request.GET.get('chapter_num')
    page_number = request.GET.get('page')
    
    title = get_object_or_404(GraphicTitle, id=title_id)
    chapter = GraphicTitleChapter.objects.get(chapter_number=chapter_number, title=title)
    page = GraphicTitlePage.objects.get(chapter=chapter, page_number=page_number)
    
    # use urls
    page_image = page.image.url
    
    # for user selection
    chapter_amount = GraphicTitleChapter.objects.filter(title=title).count()
    pages_amount = GraphicTitlePage.objects.filter(chapter=chapter).count()
    
    context = {
        'title': title,
        'current_chapter': chapter,
        'page_image': page_image,
        'chapters_amount': chapter_amount,
        'pages_amount': pages_amount
    }
    
    return render(request, 'reader/read_graphic.html', context)