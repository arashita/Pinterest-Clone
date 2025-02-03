from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from django.http import JsonResponse

def register(request):
    """Handles user registration."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('users:home')  
        else:
            for fields, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{fields}: {error}")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    """Handles user login."""
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'users:home')
            return redirect(next_url)  
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    """Handles user logout."""
    logout(request)
    return redirect('index') 

@login_required
def profile(request):
    """Display user profile."""
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "username": request.user.username,
                "email": request.user.email,
                "bio": request.user.bio,
                "profile_picture": request.user.profile_picture.url if request.user.profile_picture else None
            })
        else:
            return JsonResponse({"error": "Invalid data."}, status=400)
            
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def home(request):
    """Home page after login."""
    return render(request, "home.html")

