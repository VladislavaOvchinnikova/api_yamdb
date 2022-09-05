from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    ]
    username = models.TextField(
        'Имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
    )
    first_name = models.TextField(
        'Имя',
        blank=True,
        max_length=150
    )
    last_name = models.TextField(
        'Фамилия',
        blank=True,
        max_length=150
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        blank=True,
        max_length=15,
        choices=ROLE_CHOICES,
        default=USER
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moder(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
