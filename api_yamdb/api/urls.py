from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewViewSet, SignUpView,
                    TitlesViewSet, TokenObtainAccessView, UsersViewSet)


v1_router = DefaultRouter()
v1_router.register(
    r'users',
    UsersViewSet, basename='users')
v1_router.register(
    r'categories',
    CategoriesViewSet, basename='categories')
v1_router.register(
    r'genres',
    GenresViewSet, basename='genres')
v1_router.register(
    r'titles',
    TitlesViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainAccessView.as_view(), name='token'),
    path('v1/', include(v1_router.urls)),
]
