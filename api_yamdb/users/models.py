from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from .constants import (ADMIN, MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME,
                        MODERATOR, PROFILE_ENDPOINT_NAME, USER)


def validate_profile_endpoint_name(value):
    if value == PROFILE_ENDPOINT_NAME:
        raise ValidationError(
            f'Username {value} is forbidden'
        )


class User(AbstractUser):
    ROLES_CHOICES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        help_text=(f'Обязательное поле. Не более {MAX_LENGTH_USERNAME}'
                   ' символов. Только буквы, цифры и символы @/./+/-/_.'),
        validators=[username_validator, validate_profile_endpoint_name],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=MAX_LENGTH_EMAIL,
        help_text=(f'Обязательное поле. Не более {MAX_LENGTH_EMAIL}'
                   ' символов.'),
    )
    role = models.CharField(
        'Роль',
        max_length=max([len(_[0]) for _ in ROLES_CHOICES]),
        choices=ROLES_CHOICES,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.constraints.CheckConstraint(
                check=~models.Q(username=PROFILE_ENDPOINT_NAME),
                name='Profile endpoint name block'
            ),
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def get_confirmation_code(self):
        return default_token_generator.make_token(self)

    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)
