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
from . import views


app_name = 'reader'

urlpatterns = [
    path('title/<int:title_id>/read/type=txt/', views.read_text_title_view, name='read_text'),
    path('title/<int:title_id>/read/type=grp/', views.read_graphic_title_view, name='read_graphic'),
    path('title/<int:title_id>/read/bookmark', views.open_bookmark_view, name='open_bookmark')
]