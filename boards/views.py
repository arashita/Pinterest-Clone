from django.shortcuts import render, redirect, get_object_or_404
import json
from django.contrib.auth.decorators import login_required
from .models import Board
from posts.models import Post
from .forms import BoardForm

@login_required
def board_list(request):
    """Display all boards of the logged-in user."""
    boards = Board.objects.filter(user=request.user)
    return render(request, 'board_list.html', {'boards': boards})

@login_required
def board_create(request):
    """Allow users to create a new board."""
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid(): 
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            return redirect('boards:board_list')

    else:
        form = BoardForm()
    return render(request, 'board_form.html', {'form': form})


@login_required
def board_update(request, board_id):
    """Allow users to edit their board."""
    board = get_object_or_404(Board, id=board_id, user=request.user)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('board_list')
    else:
        form = BoardForm(instance=board)
    return render(request, 'board_form.html', {'form': form})

@login_required
def board_delete(request, board_id):
    """Allow users to delete their board."""
    board = get_object_or_404(Board, id=board_id, user=request.user)
    if request.method == "POST":
        board.delete()
        return redirect('boards:board_list')  # Redirect to the board list page
    return render(request, 'board_confirm_delete.html', {'board': board})

@login_required
def board_detail(request, board_id):
    """Ensure only board owners can manage their board."""
    board = get_object_or_404(Board, id=board_id)

    # Restrict board access
    if board.user != request.user:
        return redirect('boards:board_list')  # Redirect if the board isn't theirs

    posts = Post.objects.filter(board=board)
    return render(request, "board_detail.html", {"board": board, "posts": posts})
