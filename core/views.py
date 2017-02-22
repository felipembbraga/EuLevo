# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.views import JSONWebTokenAPIView

from .models import Profile, UserPoint, Device
from .serializers import ProfileSerializer, LoginSerializer, RegisterSerializer, UserPointSerializer, DeviceSerializer, \
    UserSerializer


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


class UserPointViewSet(ModelViewSet):
    queryset = UserPoint.objects.all()
    serializer_class = UserPointSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        try:
            request.data['user'] = request.user.pk
        except AttributeError:
            pass
        if not hasattr(request.user, 'userpoint'):
            return super(UserPointViewSet, self).create(request, *args, **kwargs)
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if hasattr(request, 'user'):
            instance = request.user.userpoint
        else:
            instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        self.perform_create_with_user(serializer, request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create_with_user(self, serializer, user):
        try:
            device = Device.objects.get(dev_id=serializer.data["dev_id"])
        except Device.DoesNotExist:
            device = Device(dev_id=serializer.data["dev_id"])
        device.is_active = True
        device.reg_id = serializer.data["reg_id"]
        device.name = serializer.data.get("name") or 'device'
        device.user = user
        device.save()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Device.objects.get(dev_id=kwargs["pk"])
            serializer = self.get_serializer(instance)
            self.perform_destroy(instance)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
