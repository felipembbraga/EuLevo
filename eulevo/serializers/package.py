from rest_framework import serializers
from rest_framework.fields import empty

from eulevo.models import Package, PackageImage


class PackageSoftSerializer(serializers.ModelSerializer):
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
            'closed',
            'created_at',
            'package_images',
            'user_point',
            'get_user',
            'has_donedeal'
        ]

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
            'closed',
            'created_at',
            'package_images',
            'user_point',
            'get_user',
            'has_donedeal',
            'get_travel',
            'count_deals'
        ]


class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = [
            'pk',
            'package',
            'image'
        ]



