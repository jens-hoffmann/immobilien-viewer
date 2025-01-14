import json
import os
import requests
from celery import shared_task
from celery.worker.control import rate_limit
from django.contrib.gis.geos import Point
import io

from django.db.models import Q
from rest_framework.parsers import JSONParser

from ImmobilienViewer.serializers import ImmobilienSerializer
from core.models import Immobilie, Region


@shared_task(name='handle_failed_django_task', queue='django_dead_letter')
def handle_failed_django_task( message: str):
    raise Exception(f"Failed task with payload: {message}")

@shared_task(name='update_map_locations', queue='djangotasks', rate_limit='60/m')
def update_map_locations(immobilie_uuid):

    url = os.environ.get('NOMINATIM_URL', 'http://nominatim:8080') + "/search"
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

@shared_task(name='update_all_regions', queue='djangotasks', rate_limit='60/m')
def update_all_regions():
    url = os.environ.get('NOMINATIM_URL', 'http://nominatim:8080') + "/reverse"
    if url is None:
        raise ConnectionError(f"Invalid nominatim url {url}")

    immobilien_list = Immobilie.objects.filter(map_location__isnull=False)
    regions = Region.objects.all()

    for immobilie in immobilien_list:
        params = {
            "lat": immobilie.lat_lng[0],
            "lon": immobilie.lat_lng[1],
            "format": "jsonv2"
        }
        response = requests.request("GET", url, params=params)
        if response.status_code == 200:
            result_list = json.loads(response.text)
            if isinstance(result_list, dict):
                adress_dict = result_list["address"]
                for region in regions:
                    search_list = []
                    if "town" in adress_dict:
                        search_list.append(adress_dict["town"])
                    if "municipality" in adress_dict:
                        search_list.append(adress_dict["municipality"])
                    if "town" in adress_dict:
                        search_list.append(adress_dict["town"])

                    found_regions = region.districts.filter(name__in=search_list)
                    if len(found_regions) > 0:
                        immobilie.regions.add(region)
                        immobilie._meta.auto_created = True
                        immobilie.save()
                        immobilie._meta.auto_created = False
                        return f"Updated region {region} for {immobilie.title}"
        else:
            handle_failed_django_task.delay(
                f"Nominatim response {response.status_code}  Reverse query failed for map location {immobilie.lat_lng}")

@shared_task(name='update_immobilie_regions', queue='djangotasks', rate_limit='60/m')
def update_immobilie_regions(immobilie_uuid):
    url = os.environ.get('NOMINATIM_URL', 'http://nominatim:8080') + "/reverse"
    if url is None:
        raise ConnectionError(f"Invalid nominatim url {url}")

    immobilien_list = Immobilie.objects.filter(Q(uuid=immobilie_uuid) &
                                               Q(map_location__isnull=False))
    regions = Region.objects.all()
    if len(immobilien_list) > 0:
        immobilie = immobilien_list[0]
        params = {
            "lat": immobilie.lat_lng[0],
            "lon": immobilie.lat_lng[1],
            "format": "jsonv2"
        }
        response = requests.request("GET", url, params=params)
        if response.status_code == 200:
            result_list = json.loads(response.text)
            if isinstance(result_list, dict):
                adress_dict = result_list["address"]
                for region in regions:
                    search_list = []
                    if "town" in adress_dict:
                        search_list.append(adress_dict["town"])
                    if "municipality" in adress_dict:
                        search_list.append(adress_dict["municipality"])
                    if "town" in adress_dict:
                        search_list.append(adress_dict["town"])

                    found_regions = region.districts.filter(name__in=search_list)
                    if len(found_regions) > 0:
                        immobilie.regions.add(region)
                        immobilie._meta.auto_created = True
                        immobilie.save()
                        immobilie._meta.auto_created = False
        else:
            handle_failed_django_task.delay(
                f"Nominatim response {response.status_code}  Reverse query failed for map location {immobilie.lat_lng}")