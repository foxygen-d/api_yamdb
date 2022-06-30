from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ReviewViewSet, CommentsViewSet,
    SignUpView, TokenObtainAccessView)


v1_router = DefaultRouter()
#v1_router.register('auth/signup/', SignUpView, basename='signup')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenObtainAccessView.as_view()),
    path('v1/', include(v1_router.urls)),
]
