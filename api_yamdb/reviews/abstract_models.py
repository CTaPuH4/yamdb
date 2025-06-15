from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import TITLE_MAX_LENGTH, TITLE_SHOWING_LENGTH

User = get_user_model()


class CategoryGenreModel(models.Model):
    name = models.CharField('Название', max_length=TITLE_MAX_LENGTH)
    slug = models.SlugField(
        'Слаг',
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:TITLE_SHOWING_LENGTH]


class CommentReviewModel(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.author.username} - {self.text}'[:TITLE_SHOWING_LENGTH]
