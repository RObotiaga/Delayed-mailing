from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='почта', unique=True)
    full_name = models.CharField(max_length=250, verbose_name='ФИО')
    about = models.TextField(verbose_name='Комментарий', blank=True)

    token = models.CharField(max_length=200, verbose_name='токен верификации', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
