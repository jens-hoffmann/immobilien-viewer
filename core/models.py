import uuid

from django.contrib.gis.db.models import PointField
from django.db import models
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from django.utils.translation import gettext_lazy as _

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class District(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    districts = models.ManyToManyField(District, blank=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class ImmobilienResource(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    base_url = models.URLField()
    crawler = models.CharField(max_length=100, null=False, blank=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Immobilie(models.Model):
    PLOT = "plot"
    HOUSE = "house"
    IMMOBIEN_TYPES = {
        PLOT: "plot",
        HOUSE: "house",
    }

    title = models.CharField(max_length=180, blank=False, null=False)
    description = models.TextField(blank=True, null=False)

    location = models.CharField(max_length=100, blank=False, null=False)
    map_location = PointField(null=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(blank=False)
    price = models.IntegerField()
    provider = models.CharField(max_length=100)
    provider_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=IMMOBIEN_TYPES)

    resource = models.ForeignKey(ImmobilienResource, on_delete=models.PROTECT, null=True, blank=True)
    regions = models.ManyToManyField(Region, blank=True)

    tags = TaggableManager(through=UUIDTaggedItem)

    @property
    def lat_lng(self):
        return list(getattr(self.map_location, 'coords', [])[::-1])

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()


class FileAttachment(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    attachment = models.FileField(upload_to='attachments/')
    immobilie = models.ForeignKey(Immobilie, on_delete=models.PROTECT, null=False, blank=False, related_name='attachments')

    def __str__(self):
        return self.name
