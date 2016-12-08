from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from core.serializers import UserSerializer
from eulevo.models import Package,PackageImage, Travel, Deal, DoneDeal


class PackageSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Package
        geo_field = 'destiny'
        fields = [
            'pk',
            'owner',
            'description',
            'weight_range',
            'destiny',
            'receiver_name',
            'receiver_phone',
            'delivery_until',
            'closed',
            'created_at'
        ]

class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = '__all__'

