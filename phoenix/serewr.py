import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
YEAR_ADDED=0
SENDER_EMAIL = "dsfsdfsd@gmail.com"
# SENDER_EMAIL_PASSWORD = "fdrD$e%65$%U^rudsf5uYuru57e4W3WrDfDFE65e45345EREE%$#%^%&^*&"
# SENDER_EMAIL_PASSWORD = "htTY67&)08&GHgFed45e43e$e56$%$%%4erTR&^"
SENDER_EMAIL_PASSWORD = "tfyYTR%^5esdfdsferttR&^%&*^$ff^rtrtRDV"
SENDER_EMAIL_PORT=587
SMTP_SERVER="smtp.gmail.com"

DEBUG=False
DEBUG=True
SECRET_KEY='-+(&pe9ld9unwos@077r(cg#_)1$^l0c##+%gpy@&95da$=_hp'
SITE_URL='/'
HOME_APP_URLS='market.urls'
PUSHER_IS_ENABLE=False
PUBLIC_ROOT="/home/khafonli/public_html/ph4/"
MYSQL=False
ALLOWED_HOSTS = ['khafonline.com','www.khafonline.com']
SITE_FULL_BASE_ADDRESS="http://khafonline.com/"





DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_origin.sqlite3',#db1 for develop
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

STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]



apps=[
    {
        'name':'web',
        'title':'وب سایت',
        'home_url':SITE_URL+"web"+"/",
    },
    {
        'name':'vehicles',
        'title':'ماشین آلات',
        'home_url':SITE_URL+"vehicles"+"/",
    },
    {
        'name':'school',
        'title':'آموزشگاه',
        'home_url':SITE_URL+"school"+"/",
    },
    {
        'name':'projectmanager',
        'title':'مدیریت پروژه',
        'home_url':SITE_URL+"projectmanager"+"/",
    },
    {
        'name':'market',
        'title':'مارکت',
        'home_url':SITE_URL+"market"+"/",
    },
    {
        'name':'mafia',
        'title':'مافیا',
        'home_url':SITE_URL+"mafia"+"/",
    },
    {
        'name':'realestate',
        'title':'املاک',
        'home_url':SITE_URL+"realestate"+"/",
    },
    {
        'name':'messenger',
        'title':'پیام رسان',
        'home_url':SITE_URL+"messenger"+"/",
    },
    {
        'name':'bms',
        'title':'ساختمان هوشمند',
        'home_url':SITE_URL+"bms"+"/",
    },
    {
        'name':'farm',
        'title':'دامپروری',
        'home_url':SITE_URL+"farm"+"/",
    },
    {
        'name':'stock',
        'title':'سهام',
        'home_url':SITE_URL+"stock"+"/",
    },
]