from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser, Follow
from posts.models import Post 
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm


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
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)  
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    """Handles user logout."""
    logout(request)
    return redirect('index') 

@login_required
def profile(request, user_id=None):
    """Display and update user profile with followers and following count."""
    
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user


    followers_count = user.followers.count()
    following_count = user.following.count()

    is_following = request.user.following.filter(following=user).exists() if request.user != user else False

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user) 
        if form.is_valid():
            updated_user = form.save()
            return JsonResponse({
                "username": updated_user.username,
                "email": updated_user.email,
                "bio": updated_user.bio,
                "profile_picture": updated_user.profile_picture.url if updated_user.profile_picture else None
            })
        else:
            return JsonResponse({"error": "Invalid data."}, status=400)

    return render(request, 'profile.html', {
        'user': user,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count
    })
    


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "home.html", {"posts": posts})



@login_required
def follow_user(request, user_id):
    """Allows a logged-in user to follow another user."""
    if request.method == "POST":
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        if user_to_follow == request.user:
            return JsonResponse({"error": "You cannot follow yourself."}, status=400)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

        if created:
            return JsonResponse({"message": "Followed successfully!"}, status=201)
        else:
            return JsonResponse({"error": "You are already following this user."}, status=400)


@login_required
def unfollow_user(request, user_id):
    """Allows a logged-in user to unfollow another user."""
    if request.method == "POST":
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
        
        if follow.exists():
            follow.delete()
            return JsonResponse({"message": "Unfollowed successfully!"}, status=200)
        else:
            return JsonResponse({"error": "You are not following this user."}, status=400)


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

@login_required
def user_list(request):
    """Display all registered users except the logged-in user."""
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, "user_list.html", {"users": users})
