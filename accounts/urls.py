from django.urls import path
from django.contrib.auth.views import LogoutView

# Importá tus vistas reales de accounts
# (En el traceback ya vimos AuthView; asumo que tenés SignupView y ProfileView)
from .views import AuthView, SignupView, ProfileView

app_name = "accounts"

urlpatterns = [
    # Login / Registro en la misma vista (lo que llamabas 'auth')
    path("auth/", AuthView.as_view(), name="auth"),

    # Signup (si tu vista de registro es separada)
    path("signup/", SignupView.as_view(), name="signup"),

    # Perfil del usuario
    path("profile/", ProfileView.as_view(), name="profile"),

    # Logout (vuelve al home cuando cierra sesión)
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
]
