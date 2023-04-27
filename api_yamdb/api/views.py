from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import (Category,
                            Genre,
                            Title,
                            Review)

from api.serializers import (CategorySerializer,
                             CommentSerializer,
                             GenreSerializer,
                             TitleSerializer,
                             ReviewSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination 

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
