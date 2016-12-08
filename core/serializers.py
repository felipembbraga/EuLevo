# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.compat import PasswordField
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import Serializer

from core.exceptions import SocialUserNotFound
from core.models import CoreUser, Profile, UserPoint

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class LoginSerializer(Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField()
    password = PasswordField(write_only=True, required=False)
    social_type = serializers.IntegerField(write_only=True, required=False)
    key = serializers.CharField(required=False)

    def validate(self, attrs):
        if all(attrs.values()):
            try:
                user = authenticate(**attrs)
            except SocialUserNotFound:
                msg = "NOT_EXIST"
                raise AuthenticationFailed(msg)

            except IntegrityError:
                msg = "INVALID_OPTIONS"
                raise AuthenticationFailed(msg)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = "WRONG_CREDENTIALS"
                raise AuthenticationFailed(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class RegisterSerializer(Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField()
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=15)
    password = PasswordField(write_only=True, max_length=128)
    social_type = serializers.IntegerField(write_only=True, required=False)
    key = serializers.CharField(required=False)

    def validate(self, attrs):
        main_fields = {'email', 'name', 'phone', 'password'}

        if not main_fields.issubset(set(attrs)):
            msg = u"FIELDS_MISSING"
            raise AuthenticationFailed(msg)
        try:
            user = CoreUser.objects.create_user(email=attrs.get('email'), password=attrs.get('password'))
        except IntegrityError:
            msg = u"EMAIL_EXIST"
            raise AuthenticationFailed(msg)
        user.profile = Profile.objects.create(user=user, name=attrs.get('name'), phone=attrs.get('phone'))

        if attrs.get('social_type') is not None and attrs.get('key') is not None:
            user.sociallogin_set.create(social_type=attrs.get('social_type'), key=attrs.get('key'))
        if user:
            payload = jwt_payload_handler(user)

            return {
                'token': jwt_encode_handler(payload),
                'user': user
            }
        else:
            msg = "Credenciais erradas"
            raise serializers.ValidationError(msg)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['pk', 'email', 'full_profile']

    def __init__(self, with_token=True, instance=None, data={}, **kwargs):
        self.with_token = with_token
        super(UserSerializer, self).__init__(instance, data, **kwargs)

    def get_fields(self):
        fields = super(UserSerializer, self).get_fields()
        if self.with_token:
            fields.append('jwt_token')
        return fields


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'name', 'phone', 'rating', 'social_image', 'image']


class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint
        fields = ['pk', 'point', 'updated_at']