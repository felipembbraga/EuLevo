from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from core.serializers import UserSerializer
from eulevo.models import Package,PackageImage, Travel, Deal, DoneDeal


class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel
        geo_field = 'destiny'
        fields = [
            'pk',
            'owner',
            'weight_range',
            'destiny',
            'destiny_description',
            'vehicle_type',
            'dt_travel',
            'blocked',
            'closed',
            'created_at',
            'updated_at',
            'user_point'
        ]
