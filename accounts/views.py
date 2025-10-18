from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import SignupForm, UserProfileForm
from .models import Profile  # Asumimos que existe un modelo Profile con OneToOne a User


class AuthView(View):
    """
    Vista unificada de Login + Signup (usa accounts/auth.html).
    En el template se usa un input hidden name="login" value="1" para diferenciar.
    """
    template_name = "accounts/auth.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "login_form": AuthenticationForm(),
                "signup_form": SignupForm(),
            },
        )

    def post(self, request):
        # Si viene el hidden login=1 -> procesar autenticación
        if request.POST.get("login") == "1":
            login_form = AuthenticationForm(request, data=request.POST)
            signup_form = SignupForm()  # vacío (solo para re-render)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                messages.success(request, "¡Bienvenido/a! Sesión iniciada correctamente.")
                return redirect("home")
            messages.error(request, "Revisa tus credenciales.")
            return render(
                request,
                self.template_name,
                {"login_form": login_form, "signup_form": signup_form},
            )

        # Caso contrario: procesar registro
        login_form = AuthenticationForm()  # vacío (solo para re-render)
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            messages.success(request, "¡Tu cuenta fue creada! Ya estás logueado/a.")
            return redirect("home")

        messages.error(request, "Por favor corrige los errores del registro.")
        return render(
            request,
            self.template_name,
            {"login_form": login_form, "signup_form": signup_form},
        )


class SignupView(View):
    """
    Registro en pantalla separada (por si querés usar /accounts/signup/).
    """
    template_name = "accounts/signup.html"

    def get(self, request):
        return render(request, self.template_name, {"form": SignupForm()})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Cuenta creada y sesión iniciada.")
            return redirect("home")
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    """
    Edición del perfil del usuario (avatar, bio, etc.).
    Asume que existe un modelo Profile con OneToOneField(User).
    Usa un formulario UserProfileForm que edita ese Profile.
    """
    template_name = "accounts/profile.html"

    def _get_profile(self, user):
        # Garantiza que el usuario tenga Profile
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        profile = self._get_profile(request.user)
        form = UserProfileForm(instance=profile)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        profile = self._get_profile(request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("profile")
        messages.error(request, "Revisa los errores del formulario.")
        return render(request, self.template_name, {"form": form})
