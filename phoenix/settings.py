
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

DEBUG = False
SERVER_ON_HEROKU=False
SERVER_ON_AZURE=False


# SECURITY WARNING: don't run with debug turned on in production!

X_FRAME_OPTIONS = 'SAMEORIGIN'

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
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.sites',   # <--
    # 'social_app',   # <--
    'django.contrib.humanize',
    'allauth',   # <--
    'allauth.account',   # <--
    'allauth.socialaccount',   # <--
    'allauth.socialaccount.providers.google', 
    'django_social_share',
    'todocalendar',
    'bms',  
    'mafia',
    'restaurant',
    'messenger',
    'realestate',
    'library',
    'tinymce',
    'school',
    'salary',
    'accounting',
    'resume',
    'vehicles',
    'help',
    'hse',
    'map',
    'tax',
    'stock',
    'authentication',
    'core',
    'dashboard',
    'farm',
    'chef',
    # 'tourleader',
    'market',
    'projectmanager',
    'phoenix_forums',
    'utility',
    'web',

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
                'core.views.DefaultContext',
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

SESSION_COOKIE_AGE = 3600 # one hour in seconds

if SERVER_ON_AZURE:
    from . import settings_azure as server_settings
elif SERVER_ON_HEROKU:
    from . import settings_heroku as server_settings
else:
    from . import server_settings

TIME_ZONE=server_settings.TIME_ZONE
SECRET_KEY=server_settings.SECRET_KEY
DEBUG=server_settings.DEBUG
STATIC_ROOT=server_settings.STATIC_ROOT
MEDIA_ROOT=server_settings.MEDIA_ROOT
STATIC_URL = server_settings.STATIC_URL
MEDIA_URL = server_settings.MEDIA_URL
MYSQL = server_settings.MYSQL
SESSION_COOKIE_AGE = server_settings.SESSION_COOKIE_AGE
SITE_URL = server_settings.SITE_URL
DATABASES = server_settings.DATABASES
YEAR_ADDED=server_settings.YEAR_ADDED
UPLOAD_ROOT=server_settings.UPLOAD_ROOT
ALLOWED_HOSTS=server_settings.ALLOWED_HOSTS
PUSHER_IS_ENABLE=server_settings.PUSHER_IS_ENABLE
STATICFILES_DIRS=server_settings.STATICFILES_DIRS
QRCODE_ROOT=os.path.join(MEDIA_ROOT,'qr_code')
SITE_FULL_BASE_ADDRESS=server_settings.SITE_FULL_BASE_ADDRESS
 


EMAIL_HOST=server_settings.EMAIL_HOST
EMAIL_PORT=server_settings.EMAIL_PORT
EMAIL_HOST_USER=server_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=server_settings.EMAIL_HOST_PASSWORD
EMAIL_USE_SSL=server_settings.EMAIL_USE_SSL
EMAIL_USE_TLS=server_settings.EMAIL_USE_TLS
SEND_EMAIL=server_settings.SEND_EMAIL

QRCODE_URL=SITE_URL+"qrcode/"
if SERVER_ON_HEROKU:
    import django_heroku
    django_heroku.settings(locals())

