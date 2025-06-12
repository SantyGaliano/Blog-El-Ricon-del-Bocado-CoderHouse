from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Vista de portada
from recipes.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Portada
    path('', HomeView.as_view(), name='home'),

    # About
    path('about/', TemplateView.as_view(template_name='recipes/about.html'), name='about'),

    # Apps
    path('recipes/', include('recipes.urls')),
    path('accounts/', include('accounts.urls')),
]

# Archivos de medios en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
