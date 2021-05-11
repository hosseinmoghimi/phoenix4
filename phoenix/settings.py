
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

DEBUG = False
SERVER_ON_HEROKU=False


if SERVER_ON_HEROKU:
    SECRET_KEY = 'django-insecure-glsp_74#5x@o7b(*o$6mc6_zd4^3$-es1h1sav5(=kstm((pn&'

# SECURITY WARNING: don't run with debug turned on in production!



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djecrety',
    'tinymce',
    'django.contrib.sites',   # <--
    # 'social_app',   # <--
    'django.contrib.humanize',
    'allauth',   # <--
    'allauth.account',   # <--
    'allauth.socialaccount',   # <--
    'allauth.socialaccount.providers.google', 


    # 'core',
    # 'authentication',
    # 'web',

]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [

        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated',]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
ROOT_URLCONF = 'phoenix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # 'core.views.CoreContext',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'phoenix.wsgi.application'




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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if SERVER_ON_HEROKU:
    from . import settings_heroku as settings_server
else:
    from . import settings_server

TIME_ZONE=settings_server.TIME_ZONE
SECRET_KEY=settings_server.SECRET_KEY
DEBUG=settings_server.DEBUG
STATIC_ROOT=settings_server.STATIC_ROOT
MEDIA_ROOT=settings_server.MEDIA_ROOT
STATIC_URL = settings_server.STATIC_URL
MEDIA_URL = settings_server.MEDIA_URL
MYSQL = settings_server.MYSQL
SITE_URL = settings_server.SITE_URL
DATABASES = settings_server.DATABASES
YEAR_ADDED=settings_server.YEAR_ADDED
ALLOWED_HOSTS=settings_server.ALLOWED_HOSTS
PUSHER_IS_ENABLE=settings_server.PUSHER_IS_ENABLE
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]

if SERVER_ON_HEROKU:
    import django_heroku
    django_heroku.settings(locals())

