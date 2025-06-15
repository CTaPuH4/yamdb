from rest_framework import filters, mixins, viewsets
from rest_framework.exceptions import MethodNotAllowed

from users.permissions import AdminOrReadOnly


class NoPutModelViewSet(viewsets.ModelViewSet):
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed(method='PUT')
        return super().update(request, *args, **kwargs)


class CategoryGenreMixin(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
