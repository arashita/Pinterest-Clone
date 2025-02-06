from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser, Follow
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm

# User Registration View
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

# User Login View
def user_login(request):
    """Handles user login."""
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)  
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

# User Logout View
@login_required
def user_logout(request):
    """Handles user logout."""
    logout(request)
    return redirect('index') 

# Profile View
@login_required
def profile(request, user_id):
    """Display user profile with follow/unfollow functionality."""
    user = get_object_or_404(CustomUser, id=user_id)

    # Check if the logged-in user is following the profile user
    is_following = request.user.following.filter(following=user).exists() if request.user != user else False
    
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

    return render(request, 'profile.html', {
        'form': form,
        'user': user,
        'is_following': is_following,
    })

# Home View
@login_required
def home(request):
    """Home page after login."""
    return render(request, "home.html", {'user': request.user})

# Follow User View
@login_required
def follow_user(request, user_id):
    """Allows a logged-in user to follow another user."""
    if request.method == "POST":
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        # Prevent self-following
        if user_to_follow == request.user:
            return JsonResponse({"error": "You cannot follow yourself."}, status=400)

        # Check if already following
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

        if created:
            return JsonResponse({"message": "Followed successfully!"}, status=201)
        else:
            return JsonResponse({"error": "You are already following this user."}, status=400)

# Unfollow User View
@login_required
def unfollow_user(request, user_id):
    """Allows a logged-in user to unfollow another user."""
    if request.method == "POST":
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

        # Check if following
        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
        
        if follow.exists():
            follow.delete()
            return JsonResponse({"message": "Unfollowed successfully!"}, status=200)
        else:
            return JsonResponse({"error": "You are not following this user."}, status=400)

# Follow Data (followers/following count) View
@login_required
def get_follow_data(request, user_id):
    """Returns follow count data for a user."""
    user = get_object_or_404(CustomUser, id=user_id)
    followers_count = user.followers.count()
    following_count = user.following.count()

    return JsonResponse({
        "followers_count": followers_count,
        "following_count": following_count
    })
