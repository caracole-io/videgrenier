"""Test settings."""
import os
from datetime import date

PROJECT = 'videgrenier'
PROJECT_VERBOSE = 'Vide Grenier'

DOMAIN_NAME = os.environ.get('DOMAIN_NAME', 'localhost')
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', f'{PROJECT}.{DOMAIN_NAME}')]
ALLOWED_HOSTS += [f'www.{host}' for host in ALLOWED_HOSTS]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

INSTALLED_APPS = [
    PROJECT,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'bootstrap4',
    'ndh',
    'testproject',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'testproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ndh.context_processors.settings_constants',
            ],
        },
    },
]

WSGI_APPLICATION = 'testproject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DB = os.environ.get('DB', 'db.sqlite3')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, DB),
    }
}
if DB == 'postgres':
    DATABASES['default'].update(
        ENGINE='django.db.backends.postgresql',
        NAME=os.environ.get('POSTGRES_DB', DB),
        USER=os.environ.get('POSTGRES_USER', DB),
        HOST=os.environ.get('POSTGRES_HOST', DB),
        PASSWORD=os.environ['POSTGRES_PASSWORD'],
    )

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

MEDIA_ROOT = '/srv/media/'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = '/srv/static/'

if os.environ.get('MEMCACHED', 'False').lower() == 'true':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'memcached:11211',
        }
    }

REPLY_TO = 'test@example.com'
DATES_VIDE_GRENIER = {
    'open': date(2018, 4, 4),
    'close': date(2018, 6, 20),
    'event': date(2018, 6, 24),
}

NDH_TEMPLATES_SETTINGS = [
    'DATES_VIDE_GRENIER',
]
