from django.urls import path
from .views import create_post, post_list, delete_post, like_post

app_name = "posts"

urlpatterns = [
    path("new/", create_post, name="create_post"),
    path("", post_list, name="post_list"),
    path("<int:post_id>/delete/", delete_post, name="delete_post"),
    path("<int:post_id>/like/", like_post, name="like_post"),
]
