import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
YEAR_ADDED=0


DEBUG=True
SECRET_KEY='-+(&pe9ld9unwos@077r(cg#_)1$^l0c##+%gpy@&95da$=_hp'
SITE_URL='/'
PUSHER_IS_ENABLE=False
PUBLIC_ROOT=BASE_DIR
MYSQL=False
ALLOWED_HOSTS = ['*']





DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    
    # 'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'OPTIONS': {
    #             'read_default_file': os.path.join(os.path.join(BASE_DIR, 'phoenix2'),'secret_pars.cnf'),

    #         },
    #     }
}

TIME_ZONE = 'Asia/Tehran'

STATIC_ROOT=os.path.join(PUBLIC_ROOT,'staticfiles')
MEDIA_ROOT=os.path.join(PUBLIC_ROOT,'media')
STATIC_URL = SITE_URL+'static/'
MEDIA_URL =  SITE_URL+'media/'
