from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

@login_required
def create_post(request):
    """Allow users to create a post only in their own boards."""
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)

            # Ensure the board belongs to the logged-in user
            if post.board.user != request.user:
                return redirect('boards:board_list')  # Redirect if board is not theirs

            post.user = request.user  # Assign post to the logged-in user
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostForm(user=request.user)  # Pass the logged-in user

    return render(request, 'create_post.html', {'form': form})


def post_list(request):
    """Display all posts."""
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "post_list.html", {"posts": posts})

def delete_post(request, post_id):
    # Get the post object by its ID, or return a 404 if it doesn't exist
    post = get_object_or_404(Post, id=post_id)

    # Ensure the user is the owner of the post (optional for security)
    if post.user == request.user:
        post.delete()  # Delete the post
        return redirect('posts:post_list')  # Redirect to the list of posts
    else:
        return redirect('home')  # Redirect if the user doesn't have permission

def like_post(request, post_id):
    # Get the post object by its ID, or return a 404 if it doesn't exist
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user has already liked the post
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Remove like
    else:
        post.likes.add(request.user)  # Add like
    
    return redirect('posts:post_list')  # Redirect to post list (or wherever you want)


@login_required
def home(request):
    """Dashboard for authenticated users."""
    return render(request, "home.html")
