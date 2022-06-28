from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentsViewSet


router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentsViewSet, basename='comments')


urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
]
