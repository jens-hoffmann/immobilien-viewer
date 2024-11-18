from rest_framework import serializers

from core.models import Immobilie


class ImmobilienSerializer(serializers.ModelSerializer):

    class Meta:
        model = Immobilie
        fields = ['uuid', 'title', 'description', 'provider', 'provider_id', 'price', 'url', 'location']
        read_only_fields = ['uuid']
