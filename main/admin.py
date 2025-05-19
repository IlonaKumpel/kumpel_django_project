from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1
    fields = ('ingredient', 'amount', 'notes')
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'difficulty', 'is_published', 'created_at')
    list_filter = ('category', 'difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'author__username', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RecipeIngredientInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'author', 'category', 'image')
        }),
        ('Детали рецепта', {
            'fields': ('difficulty', 'cooking_time', 'servings')
        }),
        ('Публикация', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)
    list_filter = ('unit',)

