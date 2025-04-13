from rest_framework import serializers
from rest_framework_gis.fields import GeometrySerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer
from django.contrib.gis.geos import Point
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from ImmobilienViewer.exceptions import ImmoblilieExistsException
from core.models import Immobilie, Region, ImmobilienResource

class ImmobilienResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImmobilienResource
        fields = ['uuid', 'name', 'base_url', 'crawler']
        read_only_fields = ['uuid']

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ['uuid', 'name']
        read_only_fields = ['uuid']


class ImmobilienSerializer(TaggitSerializer, serializers.ModelSerializer):

    resource = ImmobilienResourceSerializer()
    tags = TagListSerializerField(required=False)
    regions = RegionSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = Immobilie
        fields = ['uuid', 'title', 'description', 'provider', 'provider_id', 'price', 'url', 'location', 'type', 'resource', 'regions', 'tags']
        read_only_fields = ['uuid']

    def create(self, validated_data):
            provider_list = Immobilie.objects.filter(provider_id=validated_data.get('provider_id'))
            if len(provider_list) > 0:
                raise ImmoblilieExistsException
            resource = validated_data.pop('resource')
            resource_object_list = ImmobilienResource.objects.filter(**resource)
            if len(resource_object_list) > 0:
                resource_object = resource_object_list[0]
            else:
                resource_object = ImmobilienResource.objects.create(**resource)
                resource_object.save()

            immo_obj = Immobilie.objects.create(resource=resource_object, **validated_data)
            return immo_obj


class ImmobilieLocationSerializer(GeoFeatureModelSerializer):

    map_location = GeometrySerializerMethodField()

    def get_map_location(self, obj):
        return Point(obj.map_location.x, obj.map_location.y)

    class Meta:
        model = Immobilie
        geo_field = "map_location"

        fields = ('uuid', 'title', 'location')

