from django_filters import rest_framework as filters

from review.models import Titles


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Titles
        fields = ['name', 'year', 'genre', 'category']
