from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from . forms import RegisterForm


# Create your views here.
def show_user_profile(request):
    """Shows user profile page and it's info"""
    return render(request, 'users/profile.html')


def register_user(request):
    """Registers user, allow input and redirect to homepage"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
        }
    return render(request, 'users/register.html', context)


def login_user(request):
    """Tries to login user with input data"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username_received = form.cleaned_data.get('username')
            password_received = form.cleaned_data.get('password')
            user = authenticate(request, username=username_received, password=password_received)
            if user:
                login(request, user)
                return redirect('main:home')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
        }
    return render(request, 'users/login.html', context)


def logout_user(request):
    """Logs out authorized user"""
    logout(request)
    return redirect('main:home')
