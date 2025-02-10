from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm
import json
from django.views.decorators.csrf import csrf_exempt


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



@login_required
def post_list(request):
    """Display all posts with follow/unfollow status."""
    posts = Post.objects.all().select_related("user").order_by("-created_at")

    # Create a dictionary to store follow status for each post's user
    following_status = {post.user.id: request.user.following.filter(following=post.user).exists() for post in posts}

    return render(request, "post_list.html", {
        "posts": posts,
        "following_status": following_status,  # Pass this to template
    })


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





def get_comments(request, post_id):
    """Fetch all comments for a post, including nested replies."""
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post, parent=None).prefetch_related("replies")

    def serialize_comment(comment):
        """Recursive function to structure nested comments properly."""
        return {
            "id": comment.id,
            "user": comment.user.username,
            "text": comment.text,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "parent_id": comment.parent.id if comment.parent else None,  # Explicitly add parent_id
            "replies": [serialize_comment(reply) for reply in comment.replies.all()],
        }

    comments_data = [serialize_comment(comment) for comment in comments]
    return JsonResponse({"comments": comments_data})


@login_required
def add_comment(request, post_id):
    """Handles adding new comments and nested replies."""
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)

        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()
            parent_id = data.get("parent_id")  # Optional for replies
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        if not text:
            return JsonResponse({"error": "Comment cannot be empty"}, status=400)

        # Validate parent comment (if it's a reply)
        parent_comment = None
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id, post=post)

        # Create the new comment/reply
        new_comment = Comment.objects.create(
            user=request.user,
            post=post,
            text=text,
            parent=parent_comment
        )

        return JsonResponse({
            "id": new_comment.id,
            "user": new_comment.user.username,
            "text": new_comment.text,
            "created_at": new_comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "parent_id": parent_id
        })


@login_required
def delete_comment(request, comment_id):
    """Allows users to delete their own comments or any comment on their post."""
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if user has permission to delete
    if request.user != comment.user and request.user != comment.post.user:
        return JsonResponse({"success": False, "error": "You do not have permission to delete this comment"}, status=403)

    # Recursively delete the comment and all its replies
    def delete_nested_comments(comment):
        for reply in comment.replies.all():
            delete_nested_comments(reply)
        comment.delete()

    delete_nested_comments(comment)

    return JsonResponse({"success": True, "message": "Comment and all replies deleted successfully"})


@login_required
def edit_comment(request, comment_id):
    """Allows users to edit their own comments."""
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_text = data.get("text", "").strip()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        if not new_text:
            return JsonResponse({"error": "Comment cannot be empty"}, status=400)

        comment.text = new_text
        comment.save()

        return JsonResponse({
            "success": True,
            "message": "Comment updated successfully",
            "text": comment.text
        })

    return JsonResponse({"error": "Invalid request"}, status=400)