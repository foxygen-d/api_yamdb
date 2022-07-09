import django_filters


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug')
    category = django_filters.CharFilter(
        field_name='category__slug')
    name = django_filters.CharFilter(lookup_expr='contains')
    year = django_filters.NumberFilter()

    class Meta:
        fields = ['genre', 'category', 'name', 'year']
