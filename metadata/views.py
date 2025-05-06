from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from titles.models import GraphicTitle, TextTitle
from catalog.utils import redirect_to_title_page
from . models import TitleFavorite


@login_required(login_url="users:login")
def change_favorite_title_status(request, title_id=None):
    """
    Changes 'favorite' status of title for users when they press the button
    on title page
    """
    title_type = request.GET.get('title_type')
    user = request.user

    assert title_type in ['text', 'graphic']

    if title_type == 'graphic':
        title = get_object_or_404(GraphicTitle, id=title_id)
    elif title_type == 'text':
        title = get_object_or_404(TextTitle, id=title_id)
        
    content_type = ContentType.objects.get_for_model(title)
        
    if TitleFavorite.get_favorite_status(title, user):
        user.remove_title_from_favorites(title)
        TitleFavorite.objects.filter(
            user=user, 
            content_type=content_type,
            object_id=title_id).delete()
    else:
        user.add_title_to_favorites(title)
        TitleFavorite.objects.create(
            user=user,
            content_object=title,
        )

    return redirect_to_title_page(title_id, title_type, request.GET.get('section'))
