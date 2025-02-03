from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html') 

def home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'home.html')