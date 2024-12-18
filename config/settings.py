"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

print("------------------------ loading settings.py ------------------------")
# ! SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-m#d^%&t)hyi@gb)77syvla$c07z8(6iyl^z2!nu)qwct0g@8+("

# ! SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

REDIS_URL="redis://redis:6379/0"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'ninja',
    'corsheaders',  # !
    "myapp",
    "my_sse_app",
]

# ! is the middleware order important?
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # !
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True # ! For development only
ALLOWED_HOSTS = ['*']  # For development only

ROOT_URLCONF = "config.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# TODO: use environment variables for database settings
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE', default=os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')),
        'NAME': env('DB_NAME', default=os.getenv('DB_NAME', 'db.sqlite3')),
        'USER': env('DB_USER', default=os.getenv('DB_USER', 'postgres')),
        'PASSWORD': env('DB_PASSWORD', default=os.getenv('DB_PASSWORD', 'postgres')),
        'HOST': env('DB_HOST', default=os.getenv('DB_HOST', 'localhost')),
        'PORT': env('DB_PORT', default=os.getenv('DB_PORT', '5432')),
    }
}
print(DATABASES)

# AWS settings
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default=os.getenv('AWS_ACCESS_KEY_ID', 'dummy_aws_access_key_id'))
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default=os.getenv('AWS_SECRET_ACCESS_KEY', 'dummy_aws_secret_access_key'))
AWS_REGION = env('AWS_REGION', default=os.getenv('AWS_REGION', 'ap-southeast-2'))
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default=os.getenv('AWS_STORAGE_BUCKET_NAME', '5432'))

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


print("------------------------ completed loading settings.py ------------------------")