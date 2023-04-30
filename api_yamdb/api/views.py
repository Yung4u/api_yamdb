from rest_framework import filters, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from reviews.models import Title, Genre, Category, User, Review
from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly, IsAdminUser,
                          IsAdminModeratorOrAuthor)
from .serializers import (TitleGetSerializer, TitlePostSerializer,
                          GenreSerializer, CategorySerializer,
                          UserSerializer, ReviewSerializer,
                          CommentSerializer, ProfileSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


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

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=400)


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated, ])
def get_profile(request):
    if request.method == "PATCH":
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['=name', ]


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['=name', ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer


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


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModeratorOrAuthor, ]
    serializer_class = ReviewSerializer

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModeratorOrAuthor, ]
    serializer_class = CommentSerializer

    def get_review(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
