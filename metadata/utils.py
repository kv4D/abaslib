"""Functions for certain purposes within apps"""
from django.http import QueryDict
from titles.models import GraphicTitle, TextTitle
from reader.utils import get_client_ip
from metadata.models import TitleView


def update_views(request: QueryDict, title: TextTitle | GraphicTitle):
    """Creates new view entry for title and user"""
    user_ip = get_client_ip(request)
    TitleView.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None,
        content_object=title,
        user_ip=user_ip
    )
