"""
Django settings for vendor_service project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='default-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    # For building APIs without session dependency
    'rest_framework',
    # Custom app for vendor logic
    'vendors',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = "vendor_service.urls"

WSGI_APPLICATION = "vendor_service.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DB_DATABASE = config("DB_DATABASE", default="")
DB_USERNAME = config("DB_USERNAME", default="")
DB_PASSWORD = config("DB_PASSWORD", default="")
DB_HOST = config("DB_HOST", default="")
DB_PORT = config("DB_PORT", default=5432, cast=int)

DB_IS_AVAIL = all([DB_USERNAME, DB_PASSWORD, DB_DATABASE, DB_HOST, DB_PORT])

if DB_IS_AVAIL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_DATABASE,
            "USER": DB_USERNAME,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }

# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
