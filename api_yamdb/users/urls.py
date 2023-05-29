from django.urls import path, include
from rest_framework import routers

from .views import (
    UsersViewSet,
    MeView,
    signup_view,
    token_obtain_view,
)


router_v1_users = routers.DefaultRouter()
router_v1_users.register('users', UsersViewSet)


urlpatterns = [
    path('auth/token/', token_obtain_view, name='token_obtain'),
    path('auth/signup/', signup_view, name='signup'),
    path('users/me/', MeView.as_view(), name='me_view'),
    path('', include(router_v1_users.urls)),
]
