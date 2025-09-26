import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR      = Path(__file__).resolve().parent.parent
SECRET_KEY    = config('SECRET_KEY', default='django-insecure-dev-key-please-change-in-production')
DEBUG         = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '*']

# Application definition
INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'rest_framework',
  'corsheaders',
  'api',
]

MIDDLEWARE = [
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cts_backend.urls'

TEMPLATES = [
  {
    'BACKEND'  : 'django.template.backends.django.DjangoTemplates',
    'DIRS'     : [],
    'APP_DIRS' : True,
    'OPTIONS'  : {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

WSGI_APPLICATION = 'cts_backend.wsgi.application'

# Database
DATABASES = {
  'default': {
    'ENGINE' : 'django.db.backends.sqlite3',
    'NAME'   : BASE_DIR / 'db.sqlite3',
  }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.AttributeSimilarityValidator',
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

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE     = 'America/Santiago'
USE_I18N      = True
USE_TZ        = True

# Static files (CSS, JavaScript, Images)
STATIC_URL  = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES' : [
    'rest_framework.authentication.SessionAuthentication',
  ],
  'DEFAULT_PERMISSION_CLASSES'     : [
    'rest_framework.permissions.AllowAny',
  ],
  'DEFAULT_RENDERER_CLASSES'       : [
    'rest_framework.renderers.JSONRenderer',
  ],
  'DEFAULT_PAGINATION_CLASS'       : 'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE'                      : 20
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Celery Configuration
CELERY_BROKER_URL        = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND    = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT    = ['application/json']
CELERY_TASK_SERIALIZER   = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE          = TIME_ZONE

# Email Configuration
EMAIL_BACKEND        = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST           = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT           = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS        = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER      = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD  = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL   = config('DEFAULT_FROM_EMAIL', default='noreply@ctsturismo.cl')

# Logging
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'verbose': {
      'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
      'style': '{',
    },
    'simple': {
      'format': '{levelname} {message}',
      'style': '{',
    },
  },
  'handlers': {
    'console': {
      'level': 'DEBUG',
      'class': 'logging.StreamHandler',
      'formatter': 'simple',
    },
  },
  'root': {
    'handlers': ['console'],
    'level': 'INFO',
  },
  'loggers': {
      'django': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': False,
      },
      'api': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
      },
  },
}

# JWT Settings
JWT_SECRET_KEY      = config('JWT_SECRET_KEY', default=SECRET_KEY)
JWT_ALGORITHM       = 'HS256'
JWT_EXPIRATION_TIME = 10 * 60  # 10 minutes for verification tokens