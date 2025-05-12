from django.contrib import admin
from .models import GeneratorPreferences, GeneratedRecipe, GeneratedRecipeIngredient

admin.site.register(GeneratorPreferences)
admin.site.register(GeneratedRecipe)
admin.site.register(GeneratedRecipeIngredient)