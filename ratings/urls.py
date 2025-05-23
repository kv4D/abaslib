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


app_name = 'ratings'

urlpatterns = [
    path('rate/<str:title_type>/<int:title_id>/<int:rate>/',
         views.rate_title_view,
         name='rate_title'),
    path('rate/<str:title_type>/<int:title_id>/',
         views.delete_rate_title_view,
         name='delete_rate'),
]
