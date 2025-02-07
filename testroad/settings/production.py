"""
Production settings for testroad project.
"""

from .base import *
from dotenv import load_dotenv

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_value('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = get_env_value('DJANGO_ALLOWED_HOSTS').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_value('POSTGRES_DB'),
        'USER': get_env_value('POSTGRES_USER'),
        'PASSWORD': get_env_value('POSTGRES_PASSWORD'),
        'HOST': get_env_value('POSTGRES_HOST'),
        'PORT': get_env_value('POSTGRES_PORT'),
    }
}

# Email settings
EMAIL_BACKEND = get_env_value('EMAIL_BACKEND')
EMAIL_HOST = get_env_value('EMAIL_HOST')
EMAIL_PORT = int(get_env_value('EMAIL_PORT'))
EMAIL_USE_TLS = get_env_value('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = get_env_value('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_value('EMAIL_HOST_PASSWORD')

# AWS S3 settings
AWS_ACCESS_KEY_ID = get_env_value('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_value('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_value('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = get_env_value('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Additional security headers
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 