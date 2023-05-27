from django.urls import path, include
from rest_framework import routers

from .views import (
    UsersViewSet,
    MeView,
    signup_view,
    token_obtain_view,
)


router = routers.DefaultRouter()
router.register('users', UsersViewSet)


urlpatterns = [
    path(
        'auth/token/',
        token_obtain_view,
        name='token_obtain'
    ),
    path('auth/signup/', signup_view, name='signup'),
    path('users/me/', MeView.as_view(), name='self_view'),
    path('', include(router.urls)),
]
