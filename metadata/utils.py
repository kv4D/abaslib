"""Functions for certain purposes within apps"""
from django.http import QueryDict
from django.contrib.contenttypes.models import ContentType
from titles.models import GraphicTitle, TextTitle
from reader.utils import get_client_ip
from metadata.models import TitleView


def update_views(request: QueryDict, title: TextTitle | GraphicTitle):
    """Creates new view entry for title and user"""
    user_ip = get_client_ip(request)
    content_type = ContentType.objects.get_for_model(title)
    TitleView.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None,
        content_type=content_type,
        object_id=title.id,
        user_ip=user_ip
    )
