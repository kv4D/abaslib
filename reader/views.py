from django.shortcuts import render, get_object_or_404
from main.models import TextTitle, GraphicTitle, TextTitleChapter, GraphicTitleChapter, GraphicTitlePage

# Create your views here.
def read_text_title_view(request, title_id):
    """Render page with chapter's content"""
    chapter_number = request.GET.get('chapter')
    
    # if something's wrong, load the first page
    if not chapter_number:
        chapter_number = 1
    
    title = get_object_or_404(TextTitle, id=title_id)
    chapter = TextTitleChapter.objects.get(chapter_number=chapter_number, title=title)
    chapter_file = chapter.text_content
    
    with open(chapter_file.path, "r", encoding='utf-8') as file:
        chapter_content = file.read()
    
    context = {
        'title': title,
        'chapter': chapter,
        'chapter_content': chapter_content
    }
    
    return render(request, 'reader/read_text.html', context)


def read_graphic_title_view(request, title_id):
    """Render page with one of the chapter's pages"""
    chapter_number = request.GET.get('chapter_number')
    page_number = request.GET.get('page')
    
    # if something's wrong, load the first page
    if not chapter_number:
        chapter_number = 1
        
    title = get_object_or_404(GraphicTitle, id=title_id)
    chapter = GraphicTitleChapter.objects.get(chapter_number=chapter_number, title=title)
    page = GraphicTitlePage.objects.get(chapter=chapter, page_number=page_number)
    
    image = page.image.url
    context = {
        'title': title,
        'chapter': chapter,
        'image': image
    }
    return render(request, 'reader/read_graphic.html', context)