from rest_framework import viewsets


class EuLevoModelViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        if len(request.GET) > 0:
            lookups = request.GET.dict()
            self.queryset = self.queryset.filter(**lookups)
        return super(EuLevoModelViewSet, self).list(request, *args, **kwargs)


class EuLevoReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    def list(self, request, *args, **kwargs):
        if len(request.GET) > 0:
            lookups = request.GET.dict()
            self.queryset = self.queryset.filter(**lookups)
        return super(EuLevoReadOnlyModelViewSet, self).list(request, *args, **kwargs)