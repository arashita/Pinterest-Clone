from django.urls import path
from .views import user_login, register, user_logout
from . import views


urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', user_logout, name='logout'),
]