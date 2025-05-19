from django.test import TestCase
from main.models import Recipe, Category, Ingredient

class ModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Десерты", 
            slug="deserty"
        )
        self.ingredient = Ingredient.objects.create(
            name="Мука"
        )
        
    def test_category_creation(self):
        self.assertEqual(str(self.category), "Десерты")
        self.assertEqual(self.category.slug, "deserty")
        
    def test_recipe_creation(self):
        recipe = Recipe.objects.create(
            title="Пирог",
            category=self.category,
            cook_time=30
        )
        recipe.ingredients.add(self.ingredient)
        
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(recipe.category.name, "Десерты")