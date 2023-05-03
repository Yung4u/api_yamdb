from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import UniqueConstraint

from users.models import User
from api_yamdb.settings import (SLUG_MAX_LENGTH, NAME_MAX_LENGTH,
                                CHARACTERS_ON_TEXT)
from reviews.validators import validate_year


class CategoryGenre(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name', )

    def __str__(self):
        return self.name[:CHARACTERS_ON_TEXT]


class Category(CategoryGenre):

    class Meta(CategoryGenre.Meta):
        verbose_name = 'Категория'
        default_related_name = 'categories'


class Genre(CategoryGenre):

    class Meta(CategoryGenre.Meta):
        verbose_name = 'Жанр'
        default_related_name = 'genres'


class Title(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Имя',)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year, ),
    )
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(Genre,
                                   related_name='genre',
                                   verbose_name='Жанр')
    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Жанр_Произведение'
        default_related_name = 'genres_titles'

    def __str__(self):
        return (f'Ключ книги {self.title},'
                f'ключ жанра {self.genre}')


class ReviewComment(models.Model):
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    text = models.TextField('Текст')

    class Meta:
        abstract = True
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:CHARACTERS_ON_TEXT]


class Review(ReviewComment):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.IntegerField('Оценка', validators=[MinValueValidator(1),
                                MaxValueValidator(10)])

    class Meta(ReviewComment.Meta):
        verbose_name = 'Отзыв'
        constraints = [
            UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]


class Comment(ReviewComment):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')

    class Meta(ReviewComment.Meta):
        verbose_name = 'Комментарий'
