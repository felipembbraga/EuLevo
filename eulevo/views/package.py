from django.db.models import Q
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticated
from rest_framework.response import Response

from EuLevo.utils.base64Images import b64_to_image
from EuLevo.utils.viewset import EuLevoModelViewSet
from eulevo.models import Package, Travel, PackageImage
from eulevo.serializers import PackageSerializer, PackageImageSerializer
from eulevo.models import Deal


class PackageViewSet(EuLevoModelViewSet):
    """
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )

    http_method_names = ['get', 'post', 'patch']

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
            lookups = {
                'destiny__distance_lte': (travel.destiny, 5000),
                'weight_range__lte': travel.weight_range,
                'delivery_until__gte': travel.dt_travel
            }
            if hasattr(request.user, 'userpoint'):
                lookups['owner__userpoint__point__distance_lte'] = (request.user.userpoint.point, 5000)
            self.queryset = self.queryset.filter(**lookups).exclude(
                Q(owner=request.user)|Q(deal__in=Deal.objects.filter(travel=travel, status__in=(1,2,3,5))))
        else:
            request.GET['owner'] = request.user

        return super(PackageViewSet, self).list(request, *args, **kwargs)


class PackageImageViewSet(EuLevoModelViewSet):
    queryset = PackageImage.objects.all()
    serializer_class = PackageImageSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )

    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        if request.data.get('image'):
            name = request.data.get('name') or 'image'
            mimetype = request.data.get('mimetype') or 'jpg'
            request.data['image'] = b64_to_image(request.data['image'], name=name, mimetype=mimetype)

        return super(PackageImageViewSet, self).create(request, *args, **kwargs)
