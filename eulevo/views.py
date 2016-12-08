from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from EuLevo.utils.viewset import EuLevoModelViewSet
from .models import Package, Travel, PackageImage
from .serializers import PackageSerializer, PackageImageSerializer, TravelSerializer


class PackageViewSet(EuLevoModelViewSet):
    """
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )

    def create(self, request, *args, **kwargs):
        try:
            request.data['owner'] = request.user.pk
        except:
            pass
        return super(PackageViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        request.GET = request.GET.copy()
        if 'travel' in request.GET.keys():
            travel = Travel.objects.filter(pk=request.GET.get('travel'), owner=request.user).first()
            if not travel:
                import json
                data = json.dumps({
                    'error': True,
                    'message': 'Travel doesn\'t exists'
                })
                return Response(data)
            del request.GET['travel']
            self.queryset = self.queryset.filter(destiny__distance_lte=(travel.destiny, 5000))
        if 'owner' in request.GET.keys():
            request.GET['owner'] = request.user
        else:
            self.queryset = self.queryset.exclude(owner=request.user)

        return super(PackageViewSet, self).list(request, *args, **kwargs)


class PackageImageViewSet(ModelViewSet):
    queryset = PackageImage.objects.all()
    serializer_class = PackageImageSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )
    parser_classes = (MultiPartParser, FormParser,)


class TravelViewSet(EuLevoModelViewSet):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )

    def create(self, request, *args, **kwargs):
        try:
            request.data['owner'] = request.user.pk
        except:
            pass
        return super(TravelViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        request.GET = request.GET.copy()
        if 'package' in request.GET.keys():

            package = Package.objects.filter(pk=request.GET.get('package'), owner=request.user).first()
            if not package:
                import json
                data = json.dumps({
                    'error': True,
                    'message': 'Package doesn\'t exists'
                })
                return Response(data)
            del request.GET['package']
            self.queryset = self.queryset.filter(destiny__distance_lte=(package.destiny, 5000))
        if 'owner' in request.GET.keys():
            request.GET['owner'] = request.user
        else:
            self.queryset = self.queryset.exclude(owner=request.user)
        return super(TravelViewSet, self).list(request, *args, **kwargs)
