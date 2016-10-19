from rest_framework import serializers
from core.models import CoreUser, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['pk', 'email', 'jwt_token', 'full_profile']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'rating', 'social_image', 'image']