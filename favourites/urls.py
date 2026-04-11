from django.urls import path
from . import views

urlpatterns = [
    path('', views.FavouriteListCreateView.as_view(), name='favourite_list_create'),
    path('<int:pk>/', views.FavouriteDeleteView.as_view(), name='favourite_delete'),
]