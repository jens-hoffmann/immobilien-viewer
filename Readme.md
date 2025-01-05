from core.settings.base import MEDIA_URLfrom core.settings.base import BASE_DIRfrom django.conf.global_settings import MEDIA_ROOT

# Services

Django: http://localhost:8000

Prometheus: http://localhost:9090

Grafana: http://localhost:3000

RabbitMQ: http://localhost:15672

JaegerUI: http://localhost:16686

Flower: http://localhost:5555

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

## Implement models for database structure

Create migrations for core app:

>python manage.py makemigrations core

Apply them to the database: 

>python manage.py migrate

## Create super user

>python manage.py createsuperuser

## Celery commands

Show registered tasks

>celery inspect registered

Start tasks

>celery call app.tasks.update_something
 
## OpenTelemetry

* https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/django/django.html
* https://github.com/open-telemetry/opentelemetry-python/tree/main/docs/examples/django
* https://opentelemetry.io/docs/languages/python/
* https://github.com/open-telemetry/opentelemetry-python/tree/main/docs/examples


### Install dependencies

```
pip install opentelemetry-sdk
pip install opentelemetry-instrumentation-django
pip install opentelemetry-instrumentation-logging
pip install opentelemetry-exporter-otlp
pip install requests
```

add folowing lines to manage.py:

```python
from opentelemetry.instrumentation.django import DjangoInstrumentor

DjangoInstrumentor().instrument(is_sql_commentor_enabled=True)
```

### Configure SDK

https://opentelemetry.io/docs/languages/sdk-configuration/

Set environment in docker-compose

>opentelemetry-bootstrap --action=install

# GeoDjango, PostGIS and Leaflet

https://www.paulox.net/2021/07/19/maps-with-django-part-2-geodjango-postgis-and-leaflet/

## PostGIS: Postgres with GIS extensions

https://www.paulox.net/2021/07/19/maps-with-django-part-2-geodjango-postgis-and-leaflet/

https://www.youtube.com/watch?v=aEivCtavw-I

## Nominatim 

>osmium merge file1.osm file2.osm -o merged.osm

https://github.com/openwisp/django-rest-framework-gis 



# Signals



# File Upload

https://docs.djangoproject.com/en/5.1/topics/files/

settings.py
```python
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

```


# Search 

https://haystacksearch.org/

## Installing Solr

https://solr.apache.org/guide/solr/latest/deployment-guide/solr-in-docker.html

```dockerfile
  solr:
    container_name: solr
    image: solr
    ports:
      - "8983:8983"
    volumes:
      - solr-data:/var/solr
    command:
      - solr-precreate
      - haystackcore
```

## Setup Haystack

https://django-haystack.readthedocs.io/en/master/tutorial.html#installation

https://www.egrovesys.com/blog/solr-implementation-using-django-haystack/

https://coffeebytes.dev/en/searches-with-solr-with-django-haystack/

>python3 manage.py build_solr_schema > conf/solr/managed_schema


