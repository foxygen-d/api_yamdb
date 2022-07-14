from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = name.capitalize()

    def post_migration(self, sender, **kwargs):
        """Code to run after migration is completed."""
        verbosity = kwargs['verbosity']
        self.setup_permissions(verbosity=verbosity)

    def setup_permissions(self, verbosity) -> None:
        """Get and set permissions for the groups that should have them."""
        from django.contrib.auth.models import Group, Permission

        admins, created = Group.objects.get_or_create(name='admin')
        if verbosity >= 2:
            print('Setting up administrator permissions.')
        admins.permissions.set(Permission.objects.all())

    def ready(self) -> None:
        post_migrate.connect(self.post_migration, sender=self)
