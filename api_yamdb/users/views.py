from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from users.models import User
from api.permissions import IsAdminUser
from users.serializers import (UserSerializer, ProfileSerializer,
                               SignUpSerializer, TokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ["get", "post", "patch", "delete"]

    @action(methods=['patch', 'get'], detail=False, url_path='me',
            permission_classes=[IsAuthenticated, ])
    def get_profile(self, request):
        if request.method == "PATCH":
            serializer = ProfileSerializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    try:
        user, _ = User.objects.get_or_create(
            username=username,
            email=email
        )
    except IntegrityError:
        return Response('Пользователь уже существует',
                        status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation_code',
        confirmation_code,
        'yamdb@example.com',
        [email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = str(AccessToken.for_user(user))
        return Response({'token': token},
                        status=status.HTTP_200_OK)
    return Response({'confirmation_code': "Код подтверждения неверен"},
                    status=status.HTTP_400_BAD_REQUEST)
