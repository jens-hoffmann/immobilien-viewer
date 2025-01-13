from pathlib import Path
import json

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from django.conf import settings

from core.models import District


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = settings.BASE_DIR / "static/gemeinden_simplify20.geojson"
        batch_size = 1000
        batch = []
        file = options.get("geojson")
        if path.exists():
            with open(path) as fobj:
                json_obj = json.load(fobj)
                try:
                    for feature in json_obj["features"]:
                        district = District(name=feature["properties"]["GEN"])
                        district.full_clean()
                        batch.append(district)
                except ValidationError as e:
                    self.stderr.write(f"Validation error in row: {feature}. Error: {e}")
                except Exception as e:
                    self.stderr.write(f"Error in row: {feature}. Error: {e}")
        if batch:
            District.objects.bulk_create(batch)