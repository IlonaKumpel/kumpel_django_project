from django.test import TestCase
from django.urls import reverse, resolve
from main.views import recipe_list, category_detail

class URLTests(TestCase):
    def test_recipe_list_url(self):
        url = reverse('recipe_list')
        self.assertEqual(resolve(url).func, recipe_list)
        
    def test_category_detail_url(self):
        url = reverse('category_detail', args=['slug-test'])
        self.assertEqual(resolve(url).func, category_detail)