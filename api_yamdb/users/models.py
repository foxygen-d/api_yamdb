from django.db import models
from django.contrib.auth.models import Group, AbstractUser


class User(AbstractUser):
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
            ('user', 'User'),
            ('moderator', 'Moderator'),
            ('admin', 'Admin'),
        ],
        default='user'
    )
    _role = models.ForeignKey(
        Group,
        null=False,
        blank=False,
        to_field='name',
        choices=[
            ('user', 'User'),
            ('moderator', 'Moderator'),
            ('admin', 'Admin'),
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
