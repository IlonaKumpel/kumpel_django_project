from django import forms

class IngredientSearchForm(forms.Form):
    ingredients = forms.CharField(
        label='Введите ваши ингредиенты',
        widget=forms.TextInput(attrs={
            'placeholder': 'яйца, молоко, мука...',
            'class': 'form-control'
        }),
        help_text='Разделяйте запятыми'
    )