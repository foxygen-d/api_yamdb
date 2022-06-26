from django.contrib.auth.models import Group, AbstractUser
from django.db import models


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


class Review(models.Model):
    pass


class Comment(models.Model):
    pass
