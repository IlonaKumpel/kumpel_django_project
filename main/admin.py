from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, Step

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1
    fields = ('ingredient', 'amount', 'notes')
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'

class StepInline(admin.TabularInline):
    model = Step
    extra = 1
    min_num = 1
    fields = ('number', 'instruction', 'image')
    verbose_name = 'Шаг приготовления'
    verbose_name_plural = 'Шаги приготовления'

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'difficulty', 'is_published', 'created_at')
    list_filter = ('category', 'difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'author__username', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RecipeIngredientInline, StepInline]
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

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'number', 'short_instruction', 'has_image')
    list_filter = ('recipe',)
    search_fields = ('instruction', 'recipe__title')
    list_select_related = ('recipe',)
    
    def short_instruction(self, obj):
        return obj.instruction[:100] + '...' if len(obj.instruction) > 100 else obj.instruction
    short_instruction.short_description = 'Инструкция'
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Есть фото'