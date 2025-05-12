from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from main.models import Recipe, Ingredient
from django.db.models import Count, Q

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'main/recipe_detail.html', {'recipe': recipe})

def generator_view(request):
    all_ingredients = Ingredient.objects.all().order_by('name')
    selected_ingredients = request.POST.getlist('ingredients', [])
    
    context = {
        'all_ingredients': all_ingredients,
        'selected_ingredients': selected_ingredients,
    }
    
    if selected_ingredients:
        # Рецепты со ВСЕМИ выбранными ингредиентами
        full_match = Recipe.objects.annotate(
            match_count=Count('ingredients', filter=Q(ingredients__id__in=selected_ingredients))
        ).filter(
            match_count=len(selected_ingredients)
        ).distinct()
        
        # Рецепты с ЧАСТИЧНЫМ совпадением (отсортированы по количеству совпадений)
        partial_match = Recipe.objects.annotate(
            match_count=Count('ingredients', filter=Q(ingredients__id__in=selected_ingredients))
        ).filter(
            match_count__gt=0,
            match_count__lt=len(selected_ingredients)
        ).order_by('-match_count').distinct()
        
        context.update({
            'full_match_recipes': full_match,
            'partial_match_recipes': partial_match,
        })
    
    return render(request, 'main/recipe_generator.html', context)