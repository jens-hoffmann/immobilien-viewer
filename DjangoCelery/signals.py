import logging

from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from core.models import Immobilie, FileAttachment, Region
from celery import chain
from DjangoCelery.tasks import update_map_locations, update_all_regions, update_immobilie_regions


@receiver(post_save, sender=Immobilie)
def update_map_location_for_adress(sender, instance,  **kwargs):
    logger = logging.getLogger("DjangoCelery.signal")
    logger.info(f"Signal post_save from Immobilie {sender} for instance {instance}")
    task_chain = chain(update_map_locations.s(instance.uuid),  update_immobilie_regions.s(instance.uuid))()
    task_chain.apply_async()

@receiver(pre_delete, sender=FileAttachment)
def delete_attachment_file(sender, instance,  **kwargs):
    logger = logging.getLogger("DjangoCelery.signal")
    logger.info(f"Signal post_delete from FileAttachment {sender} for instance {instance}")
    instance.attachment.delete()

@receiver(post_save, sender=Region)
def update_all_immobilie_region_relations(sender, instance,  **kwargs):
    logger = logging.getLogger("DjangoCelery.signal")
    logger.info(f"Signal post_save from Region {sender} for instance {instance}")
    update_all_regions.delay()
