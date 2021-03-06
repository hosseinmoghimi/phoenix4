# Phoenix
Project Manager
Doctor Assistant
Market
Accounting
Transport


create a venv:
```bash
python -m venv venv
```
activate it in linux:
```bash
source ./venv/bin/avtivate
```
or activate it in windows:
```bash
./venv/Scripts/avtivate.bat
```
install requirement:
```python
pip install -r requirements.txt
```

put your site root address,'/' , '/phoenix/' eg:
```python
echo "SITE_URL='/'" >> phoenix/settings_pars.py
```
or for special subdomain (for example '/phoenix/'):

```python
echo "SITE_URL='/phoenix/'" >> phoenix/server_settings.py
```
generate and view secret key:
```python
rm phoenix/secret_key.py
echo "SECRET_KEY = 'yj)%c-)__z_null-_l-ned!$6*cs)_=w@g&t=0vj^wg)knwm3z'" >> phoenix/secret_key.py
python manage.py djecrety
```

fill and copy this file as /PATH_TO_YOUR_APP_FOLDER/phoenix/server_settings.py
```python

DEBUG=True
# DEBUG=False



import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
YEAR_ADDED=0


SECRET_KEY='-+(&pe9ld9unwos@077r(cg#_)1$^l0c##+%gpy@&95da$=_hp'
SITE_URL='/'
PUSHER_IS_ENABLE=False
PUBLIC_ROOT=BASE_DIR
MYSQL=False
HOME_APP_URLS='projectmanager.urls'
PUSHER_IS_ENABLE=True
ALLOWED_HOSTS = ['*']
SITE_FULL_BASE_ADDRESS="http://127.0.0.1:8000/"
SESSION_COOKIE_AGE = 3600 # one hour in seconds
UPLOAD_ROOT="d:\\uploads2"
ALLOW_REGISTER_ONLINE=False






DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db9.sqlite3',
    # }
    
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.path.join(os.path.join(BASE_DIR, 'phoenix'),'secret_mysql.cnf'),

            },
        }
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
        'has_help':False,
    },
    {
        'name':'faresume',
        'title':'رزومه',
        'home_url':SITE_URL+"faresume"+"/",
        'has_help':False,
    },
    {
        'name':'restaurant',
        'title':'رستوران',
        'home_url':SITE_URL+"restaurant"+"/",
        'has_help':False,
    },
    {
        'name':'library',
        'title':'کتابخانه',
        'home_url':SITE_URL+"library"+"/",
        'has_help':False,
    },
    {
        'name':'hse',
        'title':'ایمنی و محیط زیست',
        'home_url':SITE_URL+"hse"+"/",
        'has_help':False,
    },
    {
        'name':'accounting',
        'title':'حسابداری',
        'home_url':SITE_URL+"accounting"+"/",
        'has_help':False,
    },
    {
        'name':'tax',
        'title':'مالیات',
        'home_url':SITE_URL+"tax"+"/",
        'has_help':False,
    },
    {
        'name':'salary',
        'title':'سیستم حقوق و دستمزد',
        'home_url':SITE_URL+"salary"+"/",
        'has_help':False,
    },
    {
        'name':'vehicles',
        'title':'ماشین آلات',
        'home_url':SITE_URL+"vehicles"+"/",
        'has_help':False,
    },
    {
        'name':'school',
        'title':'آموزشگاه',
        'home_url':SITE_URL+"school"+"/",
        'has_help':False,
    },
    {
        'name':'projectmanager',
        'title':'مدیریت پروژه',
        'home_url':SITE_URL+"projectmanager"+"/",
        'has_help':True,
    },
    {
        'name':'market',
        'title':'مارکت',
        'home_url':SITE_URL+"market"+"",
        'has_help':False,
    },
    {
        'name':'mafia',
        'title':'مافیا',
        'home_url':SITE_URL+"mafia"+"/",
        'has_help':False,
    },
    {
        'name':'realestate',
        'title':'املاک',
        'home_url':SITE_URL+"realestate"+"/",
        'has_help':True,
    },
    {
        'name':'messenger',
        'title':'پیام رسان',
        'home_url':SITE_URL+"messenger"+"/",
        'has_help':False,
    },
    {
        'name':'bms',
        'title':'ساختمان هوشمند',
        'home_url':SITE_URL+"bms"+"/",
        'has_help':True,
    },
    {
        'name':'farm',
        'title':'دامپروری',
        'home_url':SITE_URL+"farm"+"/",
        'has_help':False,
    },
    {
        'name':'stock',
        'title':'سهام',
        'home_url':SITE_URL+"stock"+"/",
        'has_help':True,
    },
]


```

copy and put it in specific file:
```bash
vi phoenix/secret_key.py
```


put my sql db credential in files like right below:

```
[client]
database = your_database_name
host = your_host_name
user = your_user_name
password = your_password
default-character-set = utf8
```
for production:
```bash
rm phoenix/secret_my_sql.cnf
echo "[client]">> phoenix/secret_my_sql.cnf
echo "database = your_database_name">> phoenix/secret_my_sql.cnf
echo "host = your_host_name">> phoenix/secret_my_sql.cnf
echo "user = your_user_name">> phoenix/secret_my_sql.cnf
echo "password = your_password">> phoenix/secret_my_sql.cnf
echo "default-character-set = utf8" >> phoenix/secret_my_sql.cnf
```



migrate : 
```python
python manage.py migrate
```

create superuser : 
```python
python manage.py createsuperuser
```

collectstatic : 
```python
python manage.py collectstatic
```

https://tonyteaches.tech/django-nginx-uwsgi-tutorial/



```bash
cp ./server/phoenix.ini /etc/uwsgi/sites/phoenix.ini
cp ./server/phoenix /etc/nginx/sites-available/phoenix
```



test uwsgi:
```bash
uwsgi --http :8000 --module /home/leo/phoenix4/phoenix.wsgi
```


deploy: 
```bash
sudo vi /home/leo/phoenix/uwsgi_params
```



```bash
sudo vi /home/leo/phoenix/phoenix_uwsgi.ini
```
#copy phoenix_uwsgi.ini





```bash
sudo vi /etc/nginx/sites-available/phoenix.conf
```
#copy phoenix.conf




```bash
sudo ln -s /etc/nginx/sites-available/phoenix.conf /etc/nginx/sites-enabled/
```


uwsgi --socket phoenix.sock --module phoenix.wsgi --chmod-socket=666


```bash
uwsgi --ini phoenix_uwsgi.ini
```



vassals

```bash
cd /home/leo/phoenix/venv/
mkdir vassals
sudo ln -s /home/leo/phoenix/phoenix_uwsgi.ini /home/leo/phoenix/venv/vassals/
```



```bash
uwsgi --emperor /home/leo/phoenix/venv/vassals --uid www-data --gid www-data
```





```bash
sudo vi /etc/systemd/system/emperor.uwsgi.service
```
#copy emperor.uwsgi.service



```bash
systemctl enable emperor.uwsgi.service
systemctl start emperor.uwsgi.service
```


restart service:
```bash
sudo systemctl restart emperor.uwsgi.service
sudo /etc/init.d/nginx restart
```
