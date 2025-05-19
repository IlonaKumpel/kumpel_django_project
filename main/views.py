from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category, Ingredient
from django.db.models import Count, Q

def recipe_details_ajax(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'main/partials/recipe_detail.html', {'recipe': recipe})

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'main/recipe_list.html', {'recipes': recipes})

def create(request):
    selected_ingredient_ids = request.GET.getlist('ingredients')
    recipes = Recipe.objects.all()

    if selected_ingredient_ids:
        selected_ingredient_ids = list(map(int, selected_ingredient_ids))
        recipes = recipes.annotate(
            match_count=Count('ingredients', filter=Q(ingredients__id__in=selected_ingredient_ids))
        ).filter(match_count__gt=0).order_by('-match_count')

    ingredients = Ingredient.objects.all()

    return render(request, 'main/recipe_generator.html', {
        'recipes': recipes,
        'ingredients': ingredients,
    })

    
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
            Q(ingredients__ingredient__name__icontains=query)
        ).distinct()
    else:
        recipes = Recipe.objects.all()

    return render(request, 'main/search_page.html', {
        'recipes': recipes,
        'query': query
    })