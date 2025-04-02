"""
URL configuration for users app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = 'main'

urlpatterns = [
    path('',
        views.home_view,
        name='home'
        ),
    path(
        'upload_title/',
        views.upload_title_view,
        name='upload_title'
        ),
    path(
        'title/<int:title_id>/',
        views.title_page_view,
        name='title_page'
        ),
    path(
        'upload_chapter/title=<int:title_id>/',
        views.upload_chapter_view,
        name='upload_chapter'
        ),
    path('about_rights/',
        TemplateView.as_view(template_name="main/about_rights.html"),
        name='about_rights'
        ),
    path('title/<int:title_id>/add-to-favorites/',
        views.change_favorite_title_status,
        name='change_favorite_status'
        ),
    path(
        'text/',
        views.text_titles_view,
        name='text_titles'
        ),
    path(
        'graphic/',
        views.graphic_titles_view,
        name='graphic_titles'
        )
]
