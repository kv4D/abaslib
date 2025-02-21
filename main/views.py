from django.shortcuts import render
from users.models import UserProfile

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'user_profile': user_profile
        }
    else:
        context = {}

    return render(request, 'main/home.html', context)