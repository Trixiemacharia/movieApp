from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.MovieSearchView.as_view(), name='movie_search'),
    path('<int:movie_id>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('<int:movie_id>/trailer/', views.TrailerView.as_view(), name='movie_trailer'),
    path('tv/search/', views.TVSearchView.as_view(), name='tv_search'),
    path('tv/<int:tv_id>/', views.TVDetailView.as_view(), name='tv_detail'),
]