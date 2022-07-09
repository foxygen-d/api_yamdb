from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets, filters, status, permissions
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination)
from rest_framework_simplejwt.views import TokenViewBase
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import User, Review, Comment, Title, Category, Genre
from .filters import TitleFilter
from .serializers import (
    ReviewSerializer, CommentsSerializer,
    CategorySerializer, GenreSerializer,
    CodeTokenObtainSerializer, SignUpSerializer, TitleReadonlySerializer, TitleSerializer,
    UserAdminSerializer, UserProfileSerializer)
from .mixins import CreateRetrieveDestroyViewSet
from .permissions import (
    IsAuthorOrReadOnly,
    ProfileOwner, RolePermissions,
    RolePermissionsOrReadOnly)
from auth_yamdb.models import ConfirmationCode
from auth_yamdb.utils import bland_code_hasher, salty_code_hasher


User = get_user_model()


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create(**serializer.validated_data)
            code_to_mail = bland_code_hasher(
                *serializer.validated_data.values())
            code_to_db = salty_code_hasher(code_to_mail)
            username, mail = serializer.validated_data.values()
            send_mail(
                'Your code',
                f'Hi {username}, here is your code: {code_to_mail}',
                'DjangoClient@yandex.ru',
                [mail])
            ConfirmationCode.objects.create(username=user, value=code_to_db)
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)


class TokenObtainAccessView(TokenViewBase):
    serializer_class = CodeTokenObtainSerializer


class ProfileUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [ProfileOwner | RolePermissions]

    def get_object(self):
        return self.request.user


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [RolePermissions]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username']
    lookup_field = 'username'


class GenresViewSet(CreateRetrieveDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    permission_classes = [RolePermissionsOrReadOnly]
    search_fields = ['name']
    lookup_field = "slug"


class CategoriesViewSet(CreateRetrieveDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    permission_classes = [RolePermissionsOrReadOnly]
    search_fields = ['name']
    lookup_field = "slug"


# class TitlesViewSet(viewsets.ModelViewSet):
#     queryset = Title.objects.all()
#     serializer_class = TitleSerializer
#     pagination_class = LimitOffsetPagination
#     permission_classes = [RolePermissionsOrReadOnly]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['genre', 'name', 'year']
# 
#     def get_queryset(self):
#         queryset = Title.objects.all()
#         category = self.request.query_params.get('category')
#         if category is not None:
#             queryset = queryset.filter(category__slug__contains=category)
#         return queryset


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [RolePermissionsOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadonlySerializer
        return TitleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        title_id = serializer.data['id']
        return Response(
            TitleReadonlySerializer(Title.objects.get(pk=title_id)).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [
        RolePermissions | IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Представление для комментариев."""
    serializer_class = CommentsSerializer
    permission_classes = [
        RolePermissions | IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
