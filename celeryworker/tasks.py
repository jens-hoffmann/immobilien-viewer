import os

import requests

from celerysetup import app as celery_app

@celery_app.task(name='addimmobilie', queue="tasks")
def add_immobilie():
    webserver = os.environ.get('WEBSERVER', 'localhost:8000')
    url = f"http://{webserver}/immoviewer/api/immobilie/"

    payload = {
        "title": "my fancy title",
        "description": "my fancy description",
        "provider": "my provider",
        "price": 2000000,
        "url": "http://www.example.com",
        "location": "privat"
    }
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.status_code)
