from django.shortcuts import render, redirect, get_object_or_404
import json
from django.contrib.auth.decorators import login_required
from .models import Board
from .forms import BoardForm

@login_required
def board_list(request):
    """Display all boards of the logged-in user."""
    boards = Board.objects.filter(user=request.user)
    return render(request, 'boards/board_list.html', {'boards': boards})

@login_required
def board_create(request):
    """Allow users to create a new board."""
    if request.method == "POST":
        data = json.loads(request.body)
        form = BoardForm(data)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            return JsonResponse({'message': 'Board created successfully!'})
        
        return JsonResponse({'error': form.errors}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


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
    return render(request, 'boards/board_form.html', {'form': form})

@login_required
def board_delete(request, board_id):
    """Allow users to delete their board."""
    board = get_object_or_404(Board, id=board_id, user=request.user)
    if request.method == "POST":
        board.delete()
        return redirect('board_list')
    return render(request, 'boards/board_confirm_delete.html', {'board': board})
