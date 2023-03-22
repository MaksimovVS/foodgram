# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # is_subscribed
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
    )

    first_name = models.CharField(
        _('Имя'),
        max_length=150,
    )

    last_name = models.CharField(
        _('Фамилия'),
        max_length=150,
    )
