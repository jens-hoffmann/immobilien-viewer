import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from core.models import Immobilie
from DjangoCelery.tasks import update_map_locations


@receiver(post_save, sender=Immobilie)
def update_map_location_for_adress(sender, instance,  **kwargs):
    logger = logging.getLogger("DjangoCelery.signal")
    logger.info(f"Signal post_save from {sender} for instance {instance}")
    update_map_locations.delay(instance.uuid)