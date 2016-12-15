from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

from EuLevo.utils.viewset import EuLevoModelViewSet
from eulevo.models import Deal, DoneDeal
from eulevo.serializers import DealSerializer, DoneDealSerializer, DoneDealViewSerializer


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
        except:
            pass
        return super(DealViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(package__owner=request.user) | Q(travel__owner=request.user)).exclude(
            status__in=(3, 4, 5))
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


