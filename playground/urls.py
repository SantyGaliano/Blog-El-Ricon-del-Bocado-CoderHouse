from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

# Intentamos importar vistas reales; si fallan, usamos TemplateView como fallback
try:
    from recipes.views import HomeView, RecipeListView
    home_view = HomeView.as_view()
    list_view = RecipeListView.as_view()
except Exception:
    home_view = TemplateView.as_view(template_name="recipes/home.html")
    list_view = TemplateView.as_view(template_name="recipes/recipe_list.html")

try:
    from accounts.views import AuthView
    auth_view = AuthView.as_view()
except Exception:
    auth_view = TemplateView.as_view(template_name="accounts/auth.html")

urlpatterns = [
    path("admin/", admin.site.urls),

    # Nombres globales usados en templates
    path("", home_view, name="home"),                                         # {% url 'home' %}
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),  # {% url 'about' %}
    path("recipes/", list_view, name="recipe-list"),                          # {% url 'recipe-list' %}
    path("accounts/auth/", auth_view, name="auth"),                           # {% url 'auth' %}
    path("accounts/logout/", LogoutView.as_view(next_page="home"), name="logout"),   # {% url 'logout' %}

    # Includes de apps (detalles/crear/editar recetas, perfil, etc.)
    path("", include("recipes.urls")),
    path("accounts/", include("accounts.urls")),
]

# Media en desarrollo (avatars/fotos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
