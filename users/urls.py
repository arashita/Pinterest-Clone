from django.urls import path
from .views import user_login, register, user_logout, home, user_list
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import profile, follow_user, unfollow_user, get_follow_data

app_name = "users"

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', user_logout, name='logout'),
    

    path('profile/', profile, name='profile'), 
    path('profile/<int:user_id>/', profile, name='profile_with_id'),  

    path('users/', user_list, name='user_list'),
    path("", home, name="home"),
    
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    path("follow-data/<int:user_id>/", views.get_follow_data, name="follow_data"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
