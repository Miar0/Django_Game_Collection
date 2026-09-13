from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('platforms/', views.platform_list, name='platform_list'),
    path('<int:pk>/', views.game_detail, name='game_detail'),
]