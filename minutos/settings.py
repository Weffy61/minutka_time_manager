import os
from pathlib import Path

import dj_database_url
from environs import Env

env = Env()
env.read_env()

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'Минутка <>'

ACCEPTATION_URL = 'http://127.0.0.1:8000/signup/'


SECRET_KEY = env.str('SECRET_KEY', 'REPLACE_ME')

DEBUG = env.bool('DEBUG', True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['127.0.0.1', ])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'myaccount'
# LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'frontpage'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core.apps.CoreConfig',
    'apps.userprofile.apps.UserprofileConfig',
    'apps.team.apps.TeamConfig',
    'apps.project.apps.ProjectConfig',
    'apps.dashboard.apps.DashboardConfig',

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

ROOT_URLCONF = 'minutos.urls'

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
                'apps.team.context_processors.get_active_team',
                'apps.project.context_processors.get_active_entry'
            ],
        },
    },
]

WSGI_APPLICATION = 'minutos.wsgi.application'


DATABASES_DEV = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL', DATABASES_DEV))
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = env.str('MEDIA_URL', '/media/')
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATIC_URL = env.str('STATIC_URL', '/static/')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
