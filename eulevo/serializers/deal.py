from rest_framework import serializers
from eulevo.models import Deal, DoneDeal


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = [
            'pk',
            'package',
            'get_package',
            'travel',
            'get_travel',
            'user',
            'user_email',
            'status',
            'created_at',
            'updated_at',
            'get_donedeal'
        ]


class DoneDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoneDeal
        fields = [
            'pk',
            'deal',
            'get_deal'
        ]

    def create(self, validated_data):
        validated_data['protocol'] = DoneDeal.generate_protocol(validated_data.get('deal'))
        validated_data['token'] = DoneDeal.generate_token()
        # raise Exception(validated_data)
        return super(DoneDealSerializer, self).create(validated_data)


class DoneDealViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoneDeal
        fields = [
            'pk',
            'deal',
            'protocol',
            'token'
        ]
