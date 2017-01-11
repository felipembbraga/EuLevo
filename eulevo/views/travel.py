from django.db.models import Q
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticated
from rest_framework.response import Response

from EuLevo.utils.viewset import EuLevoModelViewSet
from eulevo.models import Package, Travel
from eulevo.serializers import TravelSerializer
from eulevo.models import Deal


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
        except AttributeError:
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
            if 'deal' in request.GET.keys():
                self.queryset = self.queryset.filter(
                    deal__in=Deal.objects.filter(package=package, status__in=(1, 2, 3))
                )
                del request.GET['deal']
            else:
                lookups = {
                    'destiny__distance_lte': (package.destiny, 5000),
                    'weight_range__gte': package.weight_range,
                    'dt_travel__lte': package.delivery_until

                }
                if hasattr(request.user, 'userpoint'):
                    lookups['owner__userpoint__point__distance_lte'] = (request.user.userpoint.point, 5000)
                self.queryset = self.queryset.filter(**lookups).exclude(
                    Q(owner=request.user) | Q(deal__in=Deal.objects.filter(package=package, status__in=(1, 2, 3, 5))))
        else:
            request.GET['owner'] = request.user
        return super(TravelViewSet, self).list(request, *args, **kwargs)
