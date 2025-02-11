from django.urls import path
from .views import create_post, post_list, delete_post, like_post, get_comments, add_comment, delete_comment, edit_comment
from .views import search_posts

app_name = "posts"

urlpatterns = [
    path("new/", create_post, name="create_post"),
    path("", post_list, name="post_list"),
    path("<int:post_id>/delete/", delete_post, name="delete_post"),
    path("<int:post_id>/like/", like_post, name="like_post"),
    path('comments/<int:post_id>/', get_comments, name='get_comments'),
    path('add-comment/<int:post_id>/', add_comment, name='add_comment'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('edit-comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('search/', search_posts, name="search_posts"),
]
