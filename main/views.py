"""Views for 'main' app, pages with content"""
from django.shortcuts import render
from users.models import UserProfile
from . models import Title

# Create your views here.
def home_view(request):
    """Renders website's home page with optional user info"""
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'user_profile': user_profile
        }
    else:
        context = {}

    return render(request, 'main/home.html', context)


def title_page_view(request, title_id: int, title_name: str):
    """Renders title's page, provides title's info"""
    title = Title.objects.get(id=title_id, title_name_eng=title_name)

    if title:
        context = {
            'title': title
        }
    else:
        context = {}
    return render(request, 'main/title_page.html', context)
