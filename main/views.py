from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category, Ingredient
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

def recipe_details_ajax(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'main/partials/recipe_detail.html', {'recipe': recipe})

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'main/recipe_list.html', {'recipes': recipes})

from django.shortcuts import render
from .models import Recipe, Ingredient
from django.db.models import Count, Q

def create(request):
    # Получаем все ингредиенты и выбранные пользователем
    all_ingredients = Ingredient.objects.all().order_by('name')
    selected_ingredient_ids = request.POST.getlist('ingredients', [])
    
    context = {
        'all_ingredients': all_ingredients,
        'selected_ingredients': selected_ingredient_ids,
    }

    if selected_ingredient_ids:
        try:
            # Конвертируем ID в числа
            selected_ingredient_ids = list(map(int, selected_ingredient_ids))
            num_selected = len(selected_ingredient_ids)
            
            # Находим рецепты, содержащие ВСЕ выбранные ингредиенты
            full_match = Recipe.objects.annotate(
                matched_ingredients=Count('ingredients', 
                    filter=Q(ingredients__id__in=selected_ingredient_ids))
            ).filter(
                matched_ingredients=num_selected
            ).distinct()
            
            # Находим рецепты, содержащие хотя бы один выбранный ингредиент
            partial_match = Recipe.objects.filter(
                ingredients__id__in=selected_ingredient_ids
            ).exclude(
                id__in=[r.id for r in full_match]
            ).annotate(
                matched_ingredients=Count('ingredients',
                    filter=Q(ingredients__id__in=selected_ingredient_ids))
            ).order_by(
                '-matched_ingredients'
            ).distinct()

            context.update({
                'full_match_recipes': full_match,
                'partial_match_recipes': partial_match,
                'ingredients_count': num_selected
            })
            
        except (ValueError, TypeError):
            # Обработка ошибок преобразования типов
            pass

    return render(request, 'main/recipe_generator.html', context)
    
def allrecipte(request):
    recipes = Recipe.objects.all()
    return render(request, 'main/recipe_list.html', {'recipes': recipes})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    recipes = Recipe.objects.filter(category=category)
    return render(request, 'main/recipe_list.html', {
        'recipes': recipes,
        'selected_category': category
    })

def recipes_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category)
    return render(request, 'main/recipe_list.html', {
        'recipes': recipes,
        'selected_category': category
    })

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'main/recipe_detail.html', {'recipe': recipe})


def searching(request):
    query = request.GET.get('q', '').strip()

    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query) |
            Q(steps__instruction__icontains=query) |
            Q(ingredients__ingredient__name__icontains=query)
        ).distinct()
    else:
        recipes = Recipe.objects.all()

    return render(request, 'main/search_page.html', {
        'recipes': recipes,
        'query': query
    })



