"""
Development settings for testroad project.
"""

from .base import *
from dotenv import load_dotenv

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-dev-key-for-development-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'testroad'),
        'USER': os.getenv('POSTGRES_USER', 'testroad_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'testroad_password'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),  # Dockerのサービス名
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Security settings for development
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Node.js path for Tailwind CSS
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd" 