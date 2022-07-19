from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class ConfirmationCode(models.Model):
    username = models.OneToOneField(
        User,
        to_field='username',
        on_delete=models.CASCADE,
        related_name='code'
    )
    value = models.TextField()
