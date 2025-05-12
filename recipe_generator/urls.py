from django.urls import path
from . import views

urlpatterns = [
    path('', views.generator_view, name='generator'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),  # ← добавили маршрут
]
