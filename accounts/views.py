from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import CreateView, View
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignupForm, UserForm, UserProfileForm

# Vista para registro individual (puedes conservarla o quitarla si no la usas):
class SignupView(CreateView):
    form_class    = SignupForm
    template_name = 'accounts/signup.html'
    success_url   = reverse_lazy('login')

# Vistas de perfil
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        user_form    = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form    = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'accounts/profile_form.html', {
        'user_form':    user_form,
        'profile_form': profile_form,
    })

# Cambio de contraseña
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/profile_form.html'
    success_url   = reverse_lazy('profile')

# Vista combinada de Login + Signup
class AuthView(View):
    template_name = 'accounts/auth.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, {
            'login_form':  AuthenticationForm(),
            'signup_form': SignupForm(),
        })

    def post(self, request):
        if 'login' in request.POST:
            login_form  = AuthenticationForm(request, data=request.POST)
            signup_form = SignupForm()
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Usuario o contraseña inválidos.")
        else:
            signup_form = SignupForm(request.POST)
            login_form  = AuthenticationForm()
            if signup_form.is_valid():
                user = signup_form.save()
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Error al registrarse. Revisa los datos.")

        return render(request, self.template_name, {
            'login_form':  login_form,
            'signup_form': signup_form,
        })
