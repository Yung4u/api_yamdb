from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .serializers import UserSerializer, AdminSerializer
from .permissions import IsAdminUser


class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = User.objects.all()
        serializer = AdminSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = AdminSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def update(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = AdminSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def patch_me(self, request):
        user = get_object_or_404(
            User,
            username=request.data.get('username'))
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(detail=True, methods=['patch'])
    def get_me(self, request):
        user = get_object_or_404(
            User,
            username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SignupViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(
                User,
                username=request.data.get('username'))
            email = request.data.get('email')
            token = default_token_generator.make_token(user)
            send_mail(
                'Confirmation_code',
                token,
                'yamdb@example.com',
                [email]
            )

            return Response(serializer.data)
        return Response(serializer.errors)


class TokenViewSet(viewsets.ViewSet):
    def create(self, request):
        user = get_object_or_404(
            User,
            username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            access_token = str(RefreshToken.for_user(user).access_token)
            return Response({
                'access': access_token
            })
        return Response({
            'detail': 'Confirmation code not valid'
        })
