from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status

from .models import User
from .serializers import (
    MeUserSerializer,
    UserSerializer,
    AuthSerializer,
    CustomTokenSerializer,
    get_user
)
from .permissions import AdminPermission


SERVICE_MAIL = 'from@yambd.ru'

USER_DOES_NOT_EXIST_ERROR = {
    'username': ['Пользователя с такими данными не существует.']
}
CONFIRMATION_INCORRECT_ERROR = {
    'confirmation_code': ['Неверный код подтверждения.']
}


def send_confirmation_code(user, email):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation code YamDB',
        f'Ваш код подтверждения: {confirmation_code}',
        SERVICE_MAIL,
        [email],
        fail_silently=False,
    )


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)
        send_confirmation_code(user, email)
        user.save()
        return Response(serializer.validated_data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain_view(request):
    serializer = CustomTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_user(username)
        if not user:
            return Response(USER_DOES_NOT_EXIST_ERROR,
                            status=status.HTTP_404_NOT_FOUND)
        elif default_token_generator.check_token(user, confirmation_code):
            return Response(get_token_for_user(user))
        return Response(CONFIRMATION_INCORRECT_ERROR,
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']


class MeView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = MeUserSerializer
    http_method_names = ['get', 'patch']

    def get_object(self):
        return self.request.user
