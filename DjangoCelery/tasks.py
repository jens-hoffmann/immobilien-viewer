import json
import os
import requests
from celery import shared_task
from django.contrib.gis.geos import Point

from core.models import Immobilie

@shared_task(name='update_map_locations', queue='djangotasks')
def update_map_locations():

    url = os.environ.get('NOMINATIM_URL', None)
    if url is None:
        raise ConnectionError(f"Invalid nominatim url {url}")
    immobilien_for_locating = Immobilie.objects.filter(map_location__isnull=True)
    for immobilie in immobilien_for_locating:
        params = {
            "q": immobilie.location,
            "format": "jsonv2"
        }
        response = requests.request("GET", url, params=params)
        if response.status_code == 200:
            result_list = json.loads(response.text)
            if len(result_list) > 0:
                latitude = float(result_list[0]['lat'])
                longitude = float(result_list[0]['lon'])
                immobilie.map_location = Point(latitude, longitude)
                immobilie.save()
            else:
                handle_failed_django_task.delay(
                    f"Address query failed for address {immobilie.location}. No address returned.")
        else:
            handle_failed_django_task.delay(f"Nominatim response {response.status_code}  Address query failed for address {immobilie.location}")

    return f"{len(immobilien_for_locating)} Immobilien were updated with map locations"

@shared_task(name='handle_failed_django_task', queue='django_dead_letter')
def handle_failed_django_task( message: str):
    raise Exception(f"Failed task with payload: {message}")