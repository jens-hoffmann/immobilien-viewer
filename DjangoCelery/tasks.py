import json
import os
import requests
from celery import shared_task
from celery.worker.control import rate_limit
from django.contrib.gis.geos import Point
import io

from rest_framework.parsers import JSONParser

from ImmobilienViewer.serializers import ImmobilienSerializer
from core.models import Immobilie

@shared_task(name='update_map_locations', queue='djangotasks', rate_limit='60/m')
def update_map_locations(immobilie_uuid):

    url = os.environ.get('NOMINATIM_URL', None)
    if url is None:
        raise ConnectionError(f"Invalid nominatim url {url}")

    immobilien_list = Immobilie.objects.filter(uuid=immobilie_uuid)
    if len(immobilien_list) > 0:
        immobilie = immobilien_list[0]
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
                Immobilie.objects.filter(uuid=immobilie_uuid).update(map_location=Point(longitude, latitude))
            else:
                handle_failed_django_task.delay(
                    f"Address query failed for address {immobilie.location}. No address returned.")
        else:
            handle_failed_django_task.delay(f"Nominatim response {response.status_code}  Address query failed for address {immobilie.location}")

        return f"Immobilie: {immobilie.title} was updated with map locations {immobilie.lat_lng}"
    else:
        return f"Error finding immobilie with uuid {immobilie_uuid}"


@shared_task(name='handle_failed_django_task', queue='django_dead_letter')
def handle_failed_django_task( message: str):
    raise Exception(f"Failed task with payload: {message}")