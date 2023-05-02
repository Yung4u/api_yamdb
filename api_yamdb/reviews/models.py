from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint

from .validators import validate_year


USER_ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(default='user', choices=USER_ROLES, max_length=150)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    username = models.CharField(blank=False, max_length=150, unique=True)
    last_name = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)


class CategoryGenre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name', )

    def __str__(self):
        return self.name[:30]


class Category(CategoryGenre):

    class Meta(CategoryGenre.Meta):
        verbose_name = 'Категория'
        default_related_name = 'categories'


class Genre(CategoryGenre):

    class Meta(CategoryGenre.Meta):
        verbose_name = 'Жанр'
        default_related_name = 'genres'


class Title(models.Model):
    name = models.CharField(max_length=256,
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


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(1),
                                MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-pub_date",)
        constraints = [
            UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
