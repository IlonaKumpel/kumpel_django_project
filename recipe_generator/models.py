# generator/models.py
from django.db import models
from django.contrib.auth import get_user_model
from main.models import Recipe, Ingredient, Category

User = get_user_model()

class GeneratorPreferences(models.Model):
    """Настройки генерации для каждого пользователя"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='generator_prefs'
    )
    preferred_categories = models.ManyToManyField(
        Category,
        blank=True,
        verbose_name='Предпочитаемые категории'
    )
    excluded_ingredients = models.ManyToManyField(
        Ingredient,
        blank=True,
        verbose_name='Исключенные ингредиенты'
    )
    difficulty_level = models.CharField(
        max_length=10,
        choices=[
            ('any', 'Любая'),
            ('easy', 'Легко'),
            ('medium', 'Средне'),
            ('hard', 'Сложно')
        ],
        default='any',
        verbose_name='Уровень сложности'
    )
    max_cooking_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Макс. время приготовления (мин)'
    )

    class Meta:
        verbose_name = 'Настройки генератора'
        verbose_name_plural = 'Настройки генераторов'

    def __str__(self):
        return f'Настройки генератора для {self.user.username}'

class GeneratedRecipe(models.Model):
    """Сгенерированные рецепты"""
    base_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Базовый рецепт'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='GeneratedRecipeIngredient',
        verbose_name='Ингредиенты'
    )
    instructions = models.TextField(verbose_name='Инструкция')
    generation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата генерации'
    )
    is_saved = models.BooleanField(
        default=False,
        verbose_name='Сохранен в кулинарную книгу'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='generated_recipes',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Сгенерированный рецепт'
        verbose_name_plural = 'Сгенерированные рецепты'
        ordering = ['-generation_date']

    def __str__(self):
        return f'Сгенерированный рецепт #{self.id}'

class GeneratedRecipeIngredient(models.Model):
    """Связь для ингредиентов в сгенерированных рецептах"""
    recipe = models.ForeignKey(
        GeneratedRecipe,
        on_delete=models.CASCADE,
        related_name='generated_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.CharField(
        max_length=50,
        verbose_name='Количество'
    )
    is_alternative = models.BooleanField(
        default=False,
        verbose_name='Альтернативный ингредиент'
    )

    class Meta:
        verbose_name = 'Ингредиент сгенерированного рецепта'
        verbose_name_plural = 'Ингредиенты сгенерированных рецептов'

    def __str__(self):
        return f'{self.amount} {self.ingredient.name}'