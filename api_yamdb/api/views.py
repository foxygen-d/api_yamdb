from rest_framework import viewsets

from reviews.models import User


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ...
    permission_classes = []
