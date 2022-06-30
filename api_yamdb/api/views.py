from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets, filters, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.views import TokenViewBase

from reviews.models import User, Review, Comment, Title, Category, Genre
from .serializers import (
    ReviewSerializer, CommentsSerializer,
    CategoriesSerializer, GenresSerializer,
    CodeTokenObtainSerializer, SignUpSerializer)
from .mixins import CreateRetrieveDestroyViewSet
from auth_yamdb.models import ConfirmationCode
from auth_yamdb.utils import bland_code_hasher, salty_code_hasher


User = get_user_model()


class SignUpView(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(**serializer.validated_data)
            code_to_mail = bland_code_hasher(
                *serializer.validated_data.values())
            code_to_db = salty_code_hasher(code_to_mail)
            username, mail = serializer.validated_data.values()
            send_mail(
                'Your code',
                f'Hi {username}, here is your stoopied code: {code_to_mail}',
                'DjangoClient@yandex.ru',
                [mail])
            ConfirmationCode.objects.create(username=user, value=code_to_db)
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)


class TokenObtainAccessView(TokenViewBase):
    serializer_class = CodeTokenObtainSerializer


class CategoriesViewSet(CreateRetrieveDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.DjangoModelPermissions]
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Представление для комментариев."""
    serializer_class = CommentsSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
