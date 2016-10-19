# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response

from core.decorators import retreive_only_owner
from .models import CoreUser, Profile
from .serializers import UserSerializer, ProfileSerializer
from rest_framework.decorators import permission_classes
import json


# Create your views here.
class SocialLoginViewSet(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = CoreUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, **kwargs):
        fields = {'email', 'socialType', 'token'}
        if not fields.issuperset(set(request.data)):
            return Response({'error': u'Campos inválidos'})
        try:
            user = CoreUser.objects.get(email=request.data.get('email'))
        except CoreUser.DoesNotExist:
            return Response({'status': 'NOT_EXIST'})
        # raise Exception(user)
        serializer = self.get_serializer(user, many=False)
        response = {'status': 'OK', 'data': serializer.data}
        return Response(response)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_destroy(self, instance):
        super(ProfileViewSet, self).perform_destroy(instance)

    @retreive_only_owner
    def destroy(self, request, *args, **kwargs):
        return super(ProfileViewSet, self).destroy(request, *args, **kwargs)

    @retreive_only_owner
    def update(self, request, *args, **kwargs):
        return super(ProfileViewSet, self).update(request, *args, **kwargs)

    @retreive_only_owner
    def partial_update(self, request, *args, **kwargs):
        return super(ProfileViewSet, self).partial_update(request, *args, **kwargs)





