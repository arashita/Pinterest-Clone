from django.shortcuts import render


def home(request):
    return render(request, 'templates/home.html')  # Render the home.html template
