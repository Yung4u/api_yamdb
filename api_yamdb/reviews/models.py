from django.contrib.auth.models import AbstractUser
from django.db import models


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
    email = models.CharField(max_length=254, blank=False)
    username = models.CharField(blank=False, max_length=150, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=25,
        unique=True,
    )


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(
        max_length=256,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category'
    )

    def __str__(self):
        return self.name
