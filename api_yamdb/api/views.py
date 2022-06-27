from rest_framework import viewsets, permission_classes

from reviews.models import User, Review, Comment


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ...
    permission_classes = []


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ...
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = ...
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
