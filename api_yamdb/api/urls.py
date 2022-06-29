from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

from .views import ReviewViewSet, CommentsViewSet


v1_router = DefaultRouter()
v1_router.register(
    'v1/token/',
    TokenObtainPairView, basename='token_obtain_pair')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
