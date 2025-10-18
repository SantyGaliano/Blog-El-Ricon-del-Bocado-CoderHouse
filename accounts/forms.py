# accounts/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# Si tu modelo de perfil se llama distinto, ajusta esta importación.
# En tu template se usa user.profile.avatar/bio, típico de un modelo Profile con OneToOne a User.
from .models import Profile


def _add_bootstrap_attrs(fields: dict):
    """
    Agrega class="form-control" y placeholder con el label a todos los widgets.
    Necesario para que funcionen bien los 'form-floating' de Bootstrap.
    """
    for name, field in fields.items():
        attrs = field.widget.attrs
        # Asegurar class form-control
        current = attrs.get("class", "")
        if "form-control" not in current:
            attrs["class"] = (current + " form-control").strip()
        # Asegurar placeholder para floating label
        attrs.setdefault("placeholder", field.label or name.capitalize())
        field.widget.attrs = attrs


class LoginForm(AuthenticationForm):
    """
    Opcional: si tu vista usa AuthenticationForm directamente, no hace falta.
    Si la referencia de la vista es LoginForm, dejala así.
    """
    username = forms.CharField(label="Usuario o Email", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_attrs(self.fields)


class SignupForm(UserCreationForm):
    """
    Formulario de registro para crear usuarios.
    Ajustá los campos según tu flujo (username puede ser email si lo definiste así).
    """
    first_name = forms.CharField(label="Nombre", max_length=150, required=False)
    last_name = forms.CharField(label="Apellido", max_length=150, required=False)
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_attrs(self.fields)


class UserForm(forms.ModelForm):
    """
    Form para editar datos básicos del usuario.
    Usado junto con UserProfileForm en 'profile_form.html'.
    """
    first_name = forms.CharField(label="Nombre", max_length=150, required=False)
    last_name = forms.CharField(label="Apellido", max_length=150, required=False)
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_attrs(self.fields)


class UserProfileForm(forms.ModelForm):
    """
    Form para editar el perfil (avatar y biografía).
    Asegurá que tu modelo Profile tenga esos campos:
      - avatar = ImageField(upload_to='...')
      - bio = TextField/CharField
    """
    class Meta:
        model = Profile
        fields = ("avatar", "bio")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_bootstrap_attrs(self.fields)
