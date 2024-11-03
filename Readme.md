## Create virtual environment

>python -m venv .venv

## Install packages

>pip install django

>pip freeze > requirements.txt

## Initialize Django project

>django-admin startproject core .

## Create sub apps

>python manage.py startapp newapp

register newapp in settings.py: add "newapp" to list "INSTALLED_APP"  

## Run development server

>python manage.py runserver

## Design database layout

## Optional: Split settings file to multiple file for different environments

1. Create folder "settings"
2. Inside create files "base.py", "local.py", "testing.py", "production.py"
3. move all content from settings.py to base.py
4. remove settings.py
5. in local.py, testing.py and production.py import settings from base.py
   >from .base import * 
6. in manage.py adjust follwing line, to load the appropriate file:
    >os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')


## Generate new secure secret key

>python manage.py shell

```python
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
```

## Move environment variable from source to .env file 

*Install python-dotenv*