from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Имя пользователя"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон"
    )

    email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )

    date_registered = models.DateField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )

    def __str__(self):
        return self.username
