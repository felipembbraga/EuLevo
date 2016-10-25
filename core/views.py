# -*- coding: utf-8 -*-
from rest_framework import mixins
from rest_framework.permissions import AllowAny, DjangoObjectPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_jwt.views import JSONWebTokenAPIView

from .models import CoreUser, Profile
from .serializers import UserSerializer, ProfileSerializer, LoginSerializer, RegisterSerializer


class SocialLoginView(JSONWebTokenAPIView):
    """
    View para login social
    """
    serializer_class = LoginSerializer


class RegisterView(JSONWebTokenAPIView):
    """
    View para registro
    """
    serializer_class = RegisterSerializer


# # Create your views here.
# class SocialLoginViewSet(mixins.CreateModelMixin, GenericViewSet):
#     """
#     """
#     permission_classes = (AllowAny,)
#     queryset = CoreUser.objects.all()
#     serializer_class = UserSerializer
#
#     def create(self, request, **kwargs):
#         """
#
#         Args:
#             request:
#             kwargs:
#
#         Returns:
#
#         """
#         fields = {'email', 'socialType', 'token'}
#         if not fields.issubset(set(request.data)):
#             return Response({'error': u'Campos inválidos'})
#         try:
#             user = CoreUser.objects.get(email=request.data.get('email'))
#         except CoreUser.DoesNotExist:
#             return Response({'status': 'NOT_EXIST'})
#         # raise Exception(user)
#
#         serializer = self.get_serializer(user, many=False)
#         response = {'status': 'OK', 'data': serializer.data}
#         return Response(response)
#
#
# # Create your views here.
# class CoreViewSet(ModelViewSet):
#     """
#     """
#     queryset = CoreUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAuthenticated, DjangoObjectPermissions)
#
#     def create(self, request, **kwargs):
#         """
#
#         Args:
#             request:
#             kwargs:
#
#         Returns:
#
#         """
#         fields = {'email', 'socialType', 'token'}
#         if not fields.issubset(set(request.data)):
#             return Response({'error': u'Campos inválidos'})
#         try:
#             user = CoreUser.objects.get(email=request.data.get('email'))
#         except CoreUser.DoesNotExist:
#             return Response({'status': 'NOT_EXIST'})
#         # raise Exception(user)
#
#         serializer = self.get_serializer(user, many=False)
#         response = {'status': 'OK', 'data': serializer.data}
#         return Response(response)


class ProfileViewSet(ModelViewSet):
    """
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )

    def perform_destroy(self, instance):
        """

        Args:
            instance:
        """
        super(ProfileViewSet, self).perform_destroy(instance)

    def destroy(self, request, *args, **kwargs):
        """

        Args:
            request:
            args:
            kwargs:

        Returns:

        """
        return super(ProfileViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """

        Args:
            request:
            args:
            kwargs:

        Returns:

        """
        return super(ProfileViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """

        Args:
            request:
            args:
            kwargs:

        Returns:

        """
        return super(ProfileViewSet, self).partial_update(request, *args, **kwargs)





