from pathlib import Path
import os

# === Paths base ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Seguridad / modo dev ===
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-no-usar-en-produccion")
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# === Apps instaladas ===
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps del proyecto
    "accounts",
    "recipes",

    # Terceros
    "ckeditor",  # Editor WYSIWYG
]

# === Middleware ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "playground.urls"

# === Templates ===
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # <proyecto>/templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # <- necesario para request en templates
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "playground.wsgi.application"

# === Base de datos (SQLite por defecto) ===
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# === Validadores de password ===
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# === Internacionalización ===
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# === Archivos estáticos ===
# En desarrollo, django.contrib.staticfiles sirve /static/ automáticamente con DEBUG=True
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # apuntá a: <proyecto>/static
STATIC_ROOT = BASE_DIR / "staticfiles"    # para collectstatic en prod

# === Archivos de usuario (media) ===
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# === Redirecciones de auth ===
LOGIN_URL = "auth"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# === CKEditor (config mínima) ===
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
    }
}

# === Por defecto IDs de modelos ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# (Opcional) Si usás CSRF en otro puerto/host podés sumar acá
# CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]
