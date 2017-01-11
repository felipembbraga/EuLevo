from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions
from rest_framework.response import Response

from EuLevo.utils.viewset import EuLevoModelViewSet
from eulevo.models import Deal, DoneDeal
from eulevo.serializers import DealSerializer, DoneDealSerializer, DoneDealViewSerializer
from eulevo.models import Package
from eulevo.models import Travel


class DealViewSet(EuLevoModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )

    http_method_names = ['get', 'post', 'patch']

    def create(self, request, *args, **kwargs):
        try:
            request.data['user'] = request.user.pk
        except AttributeError:
            pass
        return super(DealViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        request.GET = request.GET.copy()

        self.queryset = self.queryset.filter(Q(package__owner=request.user) | Q(travel__owner=request.user)).exclude(
            status__in=(3, 4, 5))

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
            self.queryset = self.queryset.filter(travel=travel)

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
            self.queryset = self.queryset.filter(package=package)
        return super(DealViewSet, self).list(request, *args, **kwargs)


class DoneDealViewSet(EuLevoModelViewSet):
    queryset = DoneDeal.objects.all()
    serializer_class = DoneDealSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoObjectPermissions,
    )

    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        self.serializer_class = DoneDealViewSerializer
        return super(DoneDealViewSet, self).list(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     try:
    #         request.data['user'] = request.user.pk
    #     except:
    #         pass
    #     return super(DoneDealViewSet, self).create(request, *args, **kwargs)


