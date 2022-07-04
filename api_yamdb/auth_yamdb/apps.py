from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'auth_yamdb'

    # def ready(self):
    #     from django.db.models.signals.import post_migrate
    #     
    #     from . import signals
