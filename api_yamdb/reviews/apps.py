from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ReviewsConfig(AppConfig):
    name = 'reviews'
    verbose_name = name.capitalize()

    def setup_permissions(self, sender, **kwargs) -> None:
        """Get and set permissions for the groups that should have them."""
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Group, Permission

        Review = self.get_model('Review')
        Comment = self.get_model('Comment')

        # get all auto-generated permissions for Review and Comment models

        review_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Review))
        comment_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Comment))

        # create new groups if DoesNotExist and assign respective permissions

        Group.objects.get_or_create(name='user')

        moderators, created = Group.objects.get_or_create(name="moderator")
        if not created:
            moderator_permissions = (
                list(filter(
                    lambda perm: perm.codename in (
                        'delete_review',
                        'change_review'),
                    review_permissions))
                + list(filter(
                    lambda perm: perm.codename in (
                        'delete_comment',
                        'change_comment'),
                    comment_permissions))
            )
            moderators.permissions.add(*moderator_permissions)

        admins, created = Group.objects.get_or_create(name="admin")
        if not created:
            admins.permissions.set(Permission.objects.all())

    # run the permissions setup only when migration is finished

    def ready(self) -> None:

        post_migrate.connect(self.setup_permissions, sender=self)
        return super().ready()
