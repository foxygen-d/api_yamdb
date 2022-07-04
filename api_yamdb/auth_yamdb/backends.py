from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .utils import salty_code_hasher


class ConfirmationCodeBackend(ModelBackend):
    def authenticate(self, request, username=None, confirmation_code=None):
        User = get_user_model()
        user = User.objects.get(username=username)
        if not user.code.value == salty_code_hasher(confirmation_code):
            raise Exception('Authentication failure')
        return user
