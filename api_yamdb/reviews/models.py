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
