from django.shortcuts import render, redirect
from posts.models import Post


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    print("Renderding index.html..")
    return render(request, 'core/templates/index.html') 

def home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    posts = Post.objects.all().select_related("user").order_by("-created_at")   
    return render(request, 'home.html', {'posts': posts})