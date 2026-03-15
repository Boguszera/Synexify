# appcore/settings.py
import os
import sys
from datetime import timedelta
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "infrastructure.orm.apps.OrmConfig",
    "infrastructure.web.apps.WebConfig",
]
AUTH_USER_MODEL = "orm.UserModel"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "appcore.urls"
WSGI_APPLICATION = "appcore.wsgi.application"

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "infrastructure.web.context_processors.user_notifications",
                "infrastructure.web.context_processors.demo_mode",
            ],
        },
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "EXCEPTION_HANDLER": "appcore.utils.custom_exception_handler",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

AUTHENTICATION_BACKENDS = [
    "infrastructure.api.auth.login_backend.LoginBackend",
]

env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


def get_env_var(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ImproperlyConfigured(f"Server configuration missing environment variable {var_name}")
    return value


LOGIN_URL = "web:login"
LOGIN_REDIRECT_URL = "web:project_list"
LOGOUT_REDIRECT_URL = "web:login"

# dynamic loading of environment variables - if key doesn't exist: default value
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = [h for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h]
DEMO_MODE = os.getenv("DEMO_MODE", "False") == "True"

CSRF_TRUSTED_ORIGINS = [
    "https://synexify.app",
    "https://www.synexify.app",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": get_env_var("DB_ENGINE"),
            "NAME": get_env_var("DB_NAME"),
            "USER": get_env_var("DB_USER"),
            "PASSWORD": get_env_var("DB_PASSWORD"),
            "HOST": get_env_var("DB_HOST"),
            "PORT": get_env_var("DB_PORT"),
        }
    }

# disable server cursors for pytest
if "pytest" in sys.modules:
    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
SECRET_KEY = get_env_var("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured("The SECRET_KEY environment variable is missing! Make sure the .env file is loaded.")
