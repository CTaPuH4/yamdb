from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.abstract_models import (CategoryGenreModel, CommentReviewModel)
from reviews.constants import (MAX_SCORE, MIN_SCORE, TITLE_MAX_LENGTH,
                               TITLE_SHOWING_LENGTH)
from reviews.validators import validate_year


class Category(CategoryGenreModel):
    class Meta(CategoryGenreModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreModel):
    class Meta(CategoryGenreModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=TITLE_MAX_LENGTH)
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=[
            validate_year,
        ]
    )
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        blank=True,
        related_name='titles',
        verbose_name='Жанры'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:TITLE_SHOWING_LENGTH]

    def get_genres(self):
        return ', '.join([genre.name for genre in self.genre.all()])
    get_genres.short_description = 'Жанры'


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'Жанры произведений'


class Review(CommentReviewModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(
                MAX_SCORE,
                message=f'Оценка не может быть выше {MAX_SCORE}'
            ),
            MinValueValidator(
                MIN_SCORE,
                message=f'Оценка не может быть ниже {MIN_SCORE}'
            ),
        ]
    )

    class Meta(CommentReviewModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='title_author_uniqueness'),
        ]
        default_related_name = 'reviews'
        verbose_name = 'обзор'
        verbose_name_plural = 'Обзоры'


class Comment(CommentReviewModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
    )

    class Meta(CommentReviewModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'комментарий',
        verbose_name_plural = 'Комментарии'
