import uuid
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    tags = models.ManyToManyField('Tag', blank=True)
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
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=False)

    location = models.CharField(max_length=100, blank=False, null=False)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(blank=False)
    price = models.IntegerField()
    provider = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    resource = models.ForeignKey(ImmobilienResource, on_delete=models.PROTECT, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title
