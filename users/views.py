from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm

def register(request):
    """Handles user registration."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('index')  
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
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)  # Redirect to home page after login
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
    return redirect('login')  # Redirect to login page after logout



# Create your views here.
