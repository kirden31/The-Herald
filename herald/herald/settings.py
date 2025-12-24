__all__ = ()

import os
import pathlib

from django.contrib.messages import constants as messages
import django.urls
from django.utils.translation import gettext_lazy as _
import dotenv

import herald.tools

dotenv.load_dotenv()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', default='not_so_secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = herald.tools.to_bool('DJANGO_DEBUG', False)

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', default='*').split()

# Your API keys
NEWS_API_KEYS = os.getenv('NEWS_API_KEYS', 'no_api_key').split()
GUARDIAN_API_KEYS = os.getenv('GUARDIAN_API_KEYS', 'no_api_key').split()

MAX_AUTH_ATTEMPTS = int(os.getenv('DJANGO_MAX_AUTH_ATTEMPTS', default='3'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Installed apps
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    # My apps
    'users.apps.UsersConfig',
    'news.apps.NewsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.CustomRequestUser',
]

if DEBUG:
    MIDDLEWARE.insert(
        0,
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS.append('debug_toolbar')

INTERNAL_IPS = [
    '127.0.0.1',
]

AUTHENTICATION_BACKENDS = [
    'users.backends.ConfigAuthBackend',
]

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'send_mail'
DEFAULT_FROM_EMAIL = os.getenv('DJANGO_MAIL', default='support@newshub.com')


ROOT_URLCONF = 'herald.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

WSGI_APPLICATION = 'herald.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

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

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('de', _('German')),
    ('nb', _('Norwegian Bokmål')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('zh-hans', _('Chinese (Simplified)')),
    ('ja', _('Japanese')),
    ('el', _('Greek')),
    ('ar', _('Arabic')),
]

LOGIN_URL = django.urls.reverse_lazy('users:login')
LOGIN_REDIRECT_URL = django.urls.reverse_lazy('users:profile')
LOGOUT_REDIRECT_URL = django.urls.reverse_lazy('users:login')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static_dev']

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
