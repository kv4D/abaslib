"""Views for user control and handling"""
from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . forms import RegisterForm, LoginForm


# Create your views here.
@login_required
def user_profile_view(request):
    """Shows user profile page and it's info"""
    user = request.user

    text_titles = user.favorite_text_titles.all()
    graphic_titles = user.favorite_graphic_titles.all()

    # unite titles and sort by date added
    favorite_titles = sorted(
        chain(text_titles, graphic_titles),
        key=lambda title: title.added_at,
        reverse=True
    )

    context = {
        'user': user,
        'favorite_titles': favorite_titles
    }

    return render(request, 'users/profile.html', context)


def register_user_view(request):
    """Registers user and redirects to homepage"""
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
        }
    return render(request, 'users/register.html', context)


def login_user_view(request):
    """Tries to login user with input data"""
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username_received = form.cleaned_data.get('username')
            password_received = form.cleaned_data.get('password')
            user = authenticate(request, username=username_received, password=password_received)
            if user:
                login(request, user)
                return redirect('catalog:home')
    else:
        form = LoginForm()
    context = {
        'form': form
        }
    return render(request, 'users/login.html', context)


def logout_user_view(request):
    """Logs out authorized user"""
    logout(request)
    return redirect('catalog:home')
