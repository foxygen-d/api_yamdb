from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from auth_yamdb.models import ConfirmationCode
from auth_yamdb.utils import bland_code_hasher, salty_code_hasher
from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import CreateRetrieveDestroyViewSet
from .permissions import (RolePermissions, RolePermissionsAuthorOrReadOnly,
                          RolePermissionsOrReadOnly)
from .serializers import (CategorySerializer, CodeTokenObtainSerializer,
                          CommentsSerializer, GenreSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleReadonlySerializer, TitleSerializer,
                          UserSerializer, UserProfileSerializer)


MAIL_SUBJECT = 'YAMDB: Your confirmation code'
MAIL_BODY = 'Hi {username}, here is your code: {code}'

User = get_user_model()


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
        code_to_mail = bland_code_hasher(
            *serializer.validated_data.values())
        code_to_db = salty_code_hasher(code_to_mail)
        username, mail = serializer.validated_data.values()
        send_mail(
            MAIL_SUBJECT,
            MAIL_BODY.format(username=username, code=code_to_mail),
            settings.SMTP_ADDRESS,
            [mail])
        ConfirmationCode.objects.create(username=user, value=code_to_db)
        return Response(serializer.validated_data)


class TokenObtainAccessView(TokenViewBase):
    serializer_class = CodeTokenObtainSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [RolePermissions]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username']
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
        serializer = UserProfileSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GenresViewSet(CreateRetrieveDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    permission_classes = [RolePermissionsOrReadOnly]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoriesViewSet(CreateRetrieveDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    permission_classes = [RolePermissionsOrReadOnly]
    search_fields = ['name']
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [RolePermissionsOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadonlySerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (RolePermissionsAuthorOrReadOnly,)
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
    permission_classes = (RolePermissionsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
