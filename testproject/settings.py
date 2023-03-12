"""Test settings."""
import os
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT = "videgrenier"
PROJECT_VERBOSE = "Vide Grenier"

DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "localhost")
ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOST", f"{PROJECT}.{DOMAIN_NAME}")]
ALLOWED_HOSTS += [f"www.{host}" for host in ALLOWED_HOSTS]


SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

INSTALLED_APPS = [
    PROJECT,
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django_bootstrap5",
    "ndh",
    "testproject",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "testproject.urls"

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
                "ndh.context_processors.settings_constants",
            ],
        },
    },
]

WSGI_APPLICATION = f"{PROJECT}.wsgi.application"

DB = os.environ.get("DB", "db.sqlite3")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / DB,
    },
}
if DB == "postgres":
    DATABASES["default"].update(
        ENGINE="django.db.backends.postgresql",
        NAME=os.environ.get("POSTGRES_DB", DB),
        USER=os.environ.get("POSTGRES_USER", DB),
        HOST=os.environ.get("POSTGRES_HOST", DB),
        PASSWORD=os.environ["POSTGRES_PASSWORD"],
    )

_APV = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{_APV}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{_APV}.MinimumLengthValidator",
    },
    {
        "NAME": f"{_APV}.CommonPasswordValidator",
    },
    {
        "NAME": f"{_APV}.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "fr")
TIME_ZONE = os.environ.get("TIME_ZONE", "Europe/Paris")
USE_I18N = True
USE_TZ = True

SITE_ID = 1

MEDIA_ROOT = "/srv/media/"
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = "/srv/static/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


REPLY_TO = "test@example.com"
DATES_VIDE_GRENIER = {
    "open": date(2019, 4, 18),
    "close": date(2019, 6, 19),
    "event": date(2019, 6, 23),
    "inscriptions": [
        date(2019, 5, 15),
        date(2019, 5, 22),
        date(2019, 5, 29),
        date(2019, 6, 5),
        date(2019, 6, 12),
        date(2019, 6, 19),
    ],
}

NDH_TEMPLATES_SETTINGS = [
    "DATES_VIDE_GRENIER",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
