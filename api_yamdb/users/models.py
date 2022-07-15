from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    email = models.EmailField(
        'Email',
        null=False,
        blank=False,
        unique=True,
    )
    role = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        choices=[
            (USER, 'User'),
            (MODERATOR, 'Moderator'),
            (ADMIN, 'Admin'),
        ],
        default='user'
    )
    _role = models.ForeignKey(
        Group,
        null=False,
        blank=False,
        to_field='name',
        choices=[
            (USER, 'User'),
            (MODERATOR, 'Moderator'),
            (ADMIN, 'Admin'),
        ],
        default='user',
        related_name='users',
        on_delete=models.SET_DEFAULT
    )
    bio = models.TextField(
        'Biography',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['username']

    def __init__(self, *args, **kwargs) -> None:
        if 'role' in kwargs and isinstance(kwargs['role'], str):
            kwargs['_role_id'] = kwargs.pop('role')
            kwargs['role'] = kwargs['_role_id']
        super().__init__(*args, **kwargs)
