import os

from celery.schedules import crontab
from datetime import timedelta

broker_url = os.environ.get('CELERY_BROKER_URL')
broker_connection_retry_on_startup = True
include = ('tasks',)
broker_connection_timeout = 60
result_backend = 'redis://redis:6379/0'

task_routes = {
    'zvg_scraping': {'queue': 'scrapingtasks'},
    'postresult' : {'queue': 'posttasks'},
    'handle_failed_task' : {'queue': 'dead_letter'}
}

result_persistent = True

beat_schedule = {
    'zvg_scraping_berlin': {
        'task': 'zvg_scraping',
        # 'schedule': crontab(hour=3),
        'schedule': timedelta(minutes=4),
        'args': ['Berlin']
    },
    'zvg_scraping_brandenburg': {
        'task': 'zvg_scraping',
        # 'schedule': crontab(hour=4),
        'schedule': timedelta(minutes=5),
        'args': ['Brandenburg']
    }
}

beat_schedule_filename = './celerybeat-schedule'