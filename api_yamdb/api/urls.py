from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, ReviewViewSet

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
