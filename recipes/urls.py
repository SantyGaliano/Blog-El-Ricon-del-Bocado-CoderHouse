from django.urls import path
from django.views.generic import TemplateView

# Importá tus vistas reales de recipes
# (HomeView ya aparece en el traceback, y RecipeListView seguramente existe en tu app)
from .views import HomeView, RecipeListView

app_name = "recipes"

urlpatterns = [
    # Home (raíz del sitio)
    path("", HomeView.as_view(), name="home"),

    # About (usa el template 'about.html' que vos ya tenés en /templates/about.html)
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),

    # Listado de recetas (coincide con {% url 'recipe-list' %})
    path("recipes/", RecipeListView.as_view(), name="recipe-list"),
]
