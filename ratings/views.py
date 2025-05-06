from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from titles.models import GraphicTitle, TextTitle
from . models import TitleRating


@login_required
def rate_title_view(request, title_type, title_id, rate):    
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
            defaults={'rate': rate})
    
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_rate_title_view(request, title_type, title_id):    
    assert title_type in ['text', 'graphic']
    
    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
    
    content_type = ContentType.objects.get_for_model(title)
    
    # delete rate
    TitleRating.objects.filter(
            content_type=content_type,
            object_id=title.id,
            user=request.user).delete()
    
    return redirect(request.META.get('HTTP_REFERER'))