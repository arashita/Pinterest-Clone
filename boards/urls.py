from django.urls import path
from .views import board_list, board_create, board_update, board_delete, board_detail
app_name = "boards" 
urlpatterns = [
    path('', board_list, name='board_list'),
    path('new/', board_create, name='board_create'),
    path('<int:board_id>/edit/', board_update, name='board_update'),
    path('<int:board_id>/delete/', board_delete, name='board_delete'),
    path('<int:board_id>/', board_detail, name='board_detail'),
]
