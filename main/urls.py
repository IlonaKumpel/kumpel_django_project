from django.urls import path
from . import views
from django.urls import path, include
from .views import searching
from django.contrib import admin


urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('create/', views.create, name='create'),
    path('all/', views.allrecipte, name='all_recipes'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/id/<int:category_id>/', views.recipes_by_category, name='recipes_by_category'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.searching, name='search'),
    path('recipe-details/<int:pk>/', views.recipe_details_ajax, name='recipe_details_ajax'),
]
