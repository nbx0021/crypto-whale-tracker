import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE SETTINGS ---
SECRET_KEY = 'django-insecure-your-secret-key-here'
DEBUG = True 
ALLOWED_HOSTS = ['*'] # Allowed all for easier Docker development
# -------------------------------

INSTALLED_APPS = [
    'daphne', # Must be at the top for ASGI support
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker', 
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- DATABASE CONFIGURATION UPDATED FOR DOCKER ---
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'crypto_streaming'),
#         'USER': os.environ.get('DB_USER', 'admin'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'adminpassword'),
#         # CHANGE: We use the service name 'postgres' from docker-compose
#         'HOST': os.environ.get('DB_HOST', 'postgres'), 
#         # CHANGE: Internal Docker port for Postgres is always 5432
#         'PORT': os.environ.get('DB_PORT', '5432'),     
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crypto_streaming', # Or 'crypto_db', use whatever you used in Spark
        'USER': 'admin',
        'PASSWORD': 'adminpassword',
        # CHANGED: Use localhost for local execution
        'HOST': '127.0.0.1', 
        # CHANGED: Use the external port exposed by Docker
        'PORT': '5433', 
    }
}
# -------------------------------------------------

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]