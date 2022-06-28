from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories, Genres
from .serializers import CategoriesSerializer, GenresSerializer
from .mixins import CreateRetrieveDestroyViewSet
from .permissions import IsAdminOrReadOnly


class CategoriesViewSet(CreateRetrieveDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
