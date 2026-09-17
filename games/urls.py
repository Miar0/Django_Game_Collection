from django.urls import path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='game_list'),
    path('filter/', views.FilteredGameListView.as_view(), name='game_filter'),
    path('new/', views.GameCreateView.as_view(), name='game_create'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('<int:pk>/edit/', views.GameUpdateView.as_view(), name='game_update'),
    path('<int:pk>/delete/', views.GameDeleteView.as_view(), name='game_delete'),

    path('platforms/', views.PlatformListView.as_view(), name='platform_list'),
    path('platforms/new/', views.PlatformCreateView.as_view(), name='platform_create'),
    path('platforms/<int:pk>/edit/', views.PlatformUpdateView.as_view(), name='platform_update'),
    path('platforms/<int:pk>/delete/', views.PlatformDeleteView.as_view(), name='platform_delete'),

    path('<int:game_pk>/reviews/new/', views.ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
]