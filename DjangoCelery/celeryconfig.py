import os
from dotenv import load_dotenv
from celery import Celery
from kombu import Queue, Exchange
load_dotenv()

app_environment = os.environ.get("APP_ENV", "local")

"""Run administrative tasks."""
if app_environment == "local":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')
elif app_environment == "prod":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
celery_app = Celery("djangoCelery")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.conf.task_queues = [
    Queue('djangotasks', Exchange('djangotasks'), routing_key='djangotasks',
          queue_arguments={'x-max-priority': 10}),
]

celery_app.conf.task_acks_late = True
celery_app.conf.task_default_priority = 5
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.worker_concurrency = 1

@celery_app.task
def add_numbers():
    return

celery_app.autodiscover_tasks()