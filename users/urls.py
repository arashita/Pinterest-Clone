from django.urls import path
from .views import user_login, register, user_logout,home
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import profile
from .views import follow_user, unfollow_user, get_follow_data

app_name = "users"
urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('profile/', profile, name='profile'),
    path("home/", home, name="home"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    path("follow-data/<int:user_id>/", get_follow_data, name="follow_data"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
