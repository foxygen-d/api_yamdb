from django.apps import AppConfig
from django.db.models.signals import post_migrate

from reviews.utils import get_csv_data


class ReviewsConfig(AppConfig):
    name = 'reviews'
    verbose_name = name.capitalize()

    def prepopulate_database(self, sender, **kwargs) -> None:
        """fill database with data from included csv files"""

        from django.contrib.auth.models import Group
        User = self.get_model('User')
        Genre = self.get_model('Genre')
        Category = self.get_model('Category')
        Title = self.get_model('Title')
        Review = self.get_model('Review')
        Comment = self.get_model('Comment')

        user_data = get_csv_data(source='users')
        for payload in user_data:
            payload['role'] = Group.objects.get(name=payload['role'])
            User.objects.get_or_create(**payload)

        for model in (Genre, Category):
            data = get_csv_data(source=model._meta.model_name)
            for payload in data:
                model.objects.get_or_create(**payload)

        title_data = get_csv_data(source='titles')
        for payload in title_data:
            payload['category'] = Category.objects.get(id=payload['category'])
            Title.objects.get_or_create(**payload)

        review_data = get_csv_data(source=Review._meta.model_name)
        for payload in review_data:
            payload['author'] = User.objects.get(id=payload['author'])
            if not Review.objects.filter(id=payload['id']).exists():
                Review.objects.create(**payload)

        comment_data = get_csv_data(source='comments')
        for payload in comment_data:
            payload['author'] = User.objects.get(id=payload['author'])
            if not Comment.objects.filter(id=payload['id']).exists():
                Comment.objects.create(**payload)

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
        post_migrate.connect(self.prepopulate_database, sender=self)
        return super().ready()
