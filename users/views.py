from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm

def register(request):
    """Handles user registration."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')  # Redirect to home page after registration
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    """Handles user login."""
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    """Handles user logout."""
    logout(request)
    return redirect('login')  # Redirect to login page after logout


# Create your views here.
