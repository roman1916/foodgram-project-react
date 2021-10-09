from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    EmailField,
    UniqueConstraint,
    ForeignKey,
    Model,
    CASCADE
)


class User(AbstractUser):
    email = EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True
    )
    username = CharField(
        verbose_name='юзернейм',
        max_length=150,
        unique=True
    )
    first_name = CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = CharField(
        verbose_name='Фамилия',
        max_length=150
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Follow(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='Подписан'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
