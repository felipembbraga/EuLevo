from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from core.serializers import UserSerializer
from eulevo.models import Package,PackageImage, Travel, Deal, DoneDeal


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        geo_field = 'destiny'
        fields = [
            'pk',
            'owner',
            'description',
            'weight_range',
            'destiny',
            'destiny_description',
            'receiver_name',
            'receiver_phone',
            'delivery_until',
            'closed',
            'created_at',
            'package_images',
            'user_point'
        ]

class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = [
            'pk',
            'package',
            'image'
        ]


