from django_filters import rest_framework

from reviews.models import Title


class TitleFilterSet(rest_framework.FilterSet):
    category = rest_framework.CharFilter(field_name='category__slug',
                                         lookup_expr='iexact')
    genre = rest_framework.CharFilter(field_name='genre__slug',
                                      lookup_expr='iexact')
    name = rest_framework.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
