from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    """
    Formulario simple para crear y editar recetas.
    Muestra los campos:
      • name
      • difficulty
      • instructions (RichTextField de CKEditor)
      • image
    """
    class Meta:
        model  = Recipe
        fields = ['name', 'difficulty', 'instructions', 'image']
