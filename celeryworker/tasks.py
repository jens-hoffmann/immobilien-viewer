import os

import requests

from celerysetup import app as celery_app
from selenium import webdriver

@celery_app.task(name='addimmobilie', queue="tasks")
def add_immobilie():
    webserver = os.environ.get('WEBSERVER', 'localhost:8000')
    selenium_service = os.environ.get('SELENIUM_SERVICE')
    url = f"http://{webserver}/immoviewer/api/immobilie/"

    scrape_url = 'http://www.google.de'

    browser = webdriver.Remote(selenium_service, options=webdriver.ChromeOptions())

    browser.get(scrape_url)
    print(browser.title)
    browser.quit()

    payload = {
        "title": "my fancy title",
        "description": "my fancy description",
        "provider": "my provider",
        "provider_id": "123",
        "price": 2000000,
        "url": "http://www.example.com",
        "location": "privat"
    }
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.status_code)
