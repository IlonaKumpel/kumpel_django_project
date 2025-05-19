from django.test import TestCase, Client
from django.urls import reverse
from main.models import Recipe, Category

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Завтраки", 
            slug="zavtraki"
        )
        self.recipe = Recipe.objects.create(
            title="Омлет",
            category=self.category,
            cook_time=10
        )
    
    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Омлет")
        
    def test_category_detail_view(self):
        url = reverse('category_detail', args=['zavtraki'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Завтраки")