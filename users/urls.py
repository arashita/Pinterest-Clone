from django.urls import path
from .views import user_login, register, user_logout,home
from . import views

app_name = "users"
urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path("home/", home, name="home"),
]
