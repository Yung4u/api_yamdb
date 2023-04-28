from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Title, Genre, Category
from .permissions import IsAuthorOrReadOnly
from .serializers import (TitleGetSerializer, TitlePostSerializer, 
                          GenreSerializer, CategorySerializer)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer
