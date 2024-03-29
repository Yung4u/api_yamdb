from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import (MAX_LENGTH,
                                EMAIL_MAX_LENGTH)


ADMIN = "admin"
MODERATOR = "moderator"
USER = "user"
ROLE = [
    (ADMIN, "Администратор"),
    (MODERATOR, "Модератор"),
    (USER, "Пользователь")
]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(default=USER,
                            choices=ROLE,
                            max_length=len(max(map(lambda x: x[0], ROLE),
                                               key=len)))
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH,
                              blank=False, unique=True)
    username = models.CharField(blank=False,
                                max_length=MAX_LENGTH, unique=True)
    last_name = models.CharField(max_length=MAX_LENGTH, blank=True)
    first_name = models.CharField(max_length=MAX_LENGTH, blank=True)

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return (self.role == ADMIN
                or self.is_superuser
                or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    def __str__(self) -> str:
        return self.username
