from django.db import models
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filters import TitleFilterSet
from api.mixins import CategoryGenreMixin, NoPutModelViewSet
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title
from users.permissions import AdminOrReadOnly, AuthorOrStaff


class CategoryViewSet(CategoryGenreMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(NoPutModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=models.Avg('reviews__score')).order_by('-year')
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet


class ReviewViewSet(NoPutModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorOrStaff)

    def get_title_object(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title_object().reviews.all().select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title_object()
        )


class CommentViewSet(NoPutModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorOrStaff)

    def get_review_object(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return get_object_or_404(title.reviews.all(),
                                 pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review_object().comments.all().select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review_object()
        )
