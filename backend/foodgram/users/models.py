# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        max_length=254,
        unique=True,
    )

    first_name = models.CharField(
        _("Имя"),
        max_length=150,
    )

    last_name = models.CharField(
        _("Фамилия"),
        max_length=150,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def is_follower_by(self, user):
        return Follow.objects.filter(user=user, author=self).exists()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = (models.UniqueConstraint(
            fields=("user", "author"),
            name="unique_follow",
        ),
        )

    def __str__(self):
        return f"{self.user} подписан на {self.author}"

    def clean(self):
        if self.user == self.author:
            raise ValidationError("Нельзя подписаться на самого себя")
