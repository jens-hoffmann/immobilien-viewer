import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app_environment = os.environ.get("APP_ENV", "LOCAL")

if app_environment == "LOCAL":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')
elif app_environment == "PRODUCTION":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')

app = Celery("CollectImmobilien")
app.conf.from_object("django.conf:settings", namespace="CELERY")
