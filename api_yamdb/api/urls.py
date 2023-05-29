from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import MeView, UsersViewSet, signup_view, token_obtain_view
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register('v1/users', UsersViewSet, basename='user')
router_v1.register('v1/categories', CategoryViewSet, basename='category')
router_v1.register('v1/genres', GenreViewSet, basename='genre')
router_v1.register('v1/titles', TitleViewSet, basename='title')
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns = [
    path('v1/auth/token/', token_obtain_view, name='token_obtain'),
    path('v1/auth/signup/', signup_view, name='signup'),
    path('v1/users/me/', MeView.as_view(), name='me_view'),
    path('', include(router_v1.urls)),
]
