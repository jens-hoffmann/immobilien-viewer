import logging

from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from core.models import Immobilie, FileAttachment
from DjangoCelery.tasks import update_map_locations


@receiver(post_save, sender=Immobilie)
def update_map_location_for_adress(sender, instance,  **kwargs):
    logger = logging.getLogger("DjangoCelery.signal")
    logger.info(f"Signal post_save from Immobilie {sender} for instance {instance}")
    update_map_locations.delay(instance.uuid)

@receiver(pre_delete, sender=FileAttachment)
def delete_attachment_file(sender, instance,  **kwargs):
    logger = logging.getLogger("DjangoCelery.signal")
    logger.info(f"Signal post_delete from FileAttachment {sender} for instance {instance}")
    instance.attachment.delete()
