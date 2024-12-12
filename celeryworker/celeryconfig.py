import os

from celery.schedules import crontab

broker_url = os.environ.get('CELERY_BROKER_URL')
broker_connection_retry_on_startup = True
include = ('tasks',)
broker_connection_timeout = 60
result_backend = 'redis://redis:6379/0'

task_routes = {
    'zvg_scraping': {'queue': 'scrapingtasks'},
    'postresult' : {'queue': 'posttasks'}
}

result_persistent = True

beat_schedule = {
    'zvg_scraping': {
        'task': 'zvg_scraping',
        'schedule': crontab(hour=3)
    }
}

beat_schedule_filename = './celerybeat-schedule'