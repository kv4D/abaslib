from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
from titles.models import GraphicTitle, TextTitle
from . models import TitleRating


# Create your views here.
def rate_title_view(request, title_id, rating):    
    title_type = request.GET.get('title_type')

    assert title_type in ['text', 'graphic']
    
    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
    
    content_type = ContentType.objects.get_for_model(title)
    
    # new rating for user
    TitleRating.objects.update_or_create(
            content_type=content_type,
            object_id=title.id,
            user=request.user, 
            rate=rating)
    
    return redirect(request.META.get('HTTP_REFERER'))