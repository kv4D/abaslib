"""Functions for certain purposes within apps"""
from django.http import QueryDict
from main.models import GraphicTitle, GraphicTitleChapter, TextTitle
from reader.models import GraphicTitleView, TextTitleView


def get_client_ip(request):
    """Get request's IP"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def process_chapter_switch(page_number,
                           chapter: GraphicTitleChapter,
                           title: GraphicTitle,
                           get_params: QueryDict):
    """Process chapter switch if required"""
    # end of the chapter
    # try to get the next chapter
    if page_number > chapter.pages.count():
        chapter = title.get_next_chapter(chapter)
        page_number = 1
        # modify get parameters
        get_params['page'] = str(page_number)
        get_params['chapter_num'] = str(chapter.chapter_number)
    # beginning of the chapter
    # try to get the previous chapter
    elif page_number <= 0:
        chapter = title.get_previous_chapter(chapter)
        page_number = chapter.pages.count()
        # modify get parameters
        get_params['page'] = str(page_number)
        get_params['chapter_num'] = str(chapter.chapter_number)
    # no switch or modifications required
    return page_number, chapter, get_params


def update_views(request: QueryDict, title: TextTitle | GraphicTitle):
    """Creates new view entry for title and user"""
    if title.title_type == 'text':
        user_ip = get_client_ip(request)
        TextTitleView.objects.get_or_create(
            user=request.user if request.user.is_authenticated else None,
            title=title,
            user_ip=user_ip
        )
    elif title.title_type == 'graphic':
        user_ip = get_client_ip(request)
        GraphicTitleView.objects.get_or_create(
            user=request.user if request.user.is_authenticated else None,
            title=title,
            user_ip=user_ip
        )
