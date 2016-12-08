from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from core.serializers import UserSerializer
from eulevo.models import Package,PackageImage, Travel, Deal, DoneDeal


class TravelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Travel
        geo_field = 'destiny'
        fields = [
            'pk',
            'owner',
            'weight_range',
            'destiny',
            'vehicle_type',
            'dt_travel',
            'blocked',
            'closed',
            'created_at',
            'updated_at'
        ]
