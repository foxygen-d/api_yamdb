from django.db import models
from django.contrib.auth.models import Group, AbstractUser


class User(AbstractUser):

    role = models.ForeignKey(
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
