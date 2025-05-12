from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampedModel):
    name = models.CharField('Название категории', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField('Иконка (FontAwesome)', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.unit})" if self.unit else self.name

class Recipe(TimeStampedModel):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
    ]

    title = models.CharField('Название', max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )
    difficulty = models.CharField(
        'Сложность',
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )
    cooking_time = models.PositiveIntegerField('Время приготовления (минуты)')
    servings = models.PositiveIntegerField('Количество порций', default=1)
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/%Y/%m/%d/',
        blank=True
    )
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
        ]
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.DecimalField(
        'Количество',
        max_digits=6,
        decimal_places=2
    )
    notes = models.CharField('Примечания', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        unique_together = ('recipe', 'ingredient')
        ordering = ['ingredient__name']

    def __str__(self):
        return f"{self.amount} {self.ingredient.unit} {self.ingredient.name}"

class Step(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    number = models.PositiveIntegerField('Шаг')
    instruction = models.TextField('Инструкция')
    image = models.ImageField(
        'Изображение',
        upload_to='steps/%Y/%m/%d/',
        blank=True
    )

    class Meta:
        verbose_name = 'Шаг приготовления'
        verbose_name_plural = 'Шаги приготовления'
        ordering = ['number']
        unique_together = ('recipe', 'number')

    def __str__(self):
        return f"Шаг {self.number} - {self.recipe.title}"