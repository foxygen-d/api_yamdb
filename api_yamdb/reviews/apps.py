from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate

from reviews.utils import set_by_id, get_csv_data


class ReviewsConfig(AppConfig):
    name = 'reviews'
    verbose_name = name.capitalize()

    def post_migration(self, sender, **kwargs):
        """Code to run after migration is completed."""
        verbosity = kwargs['verbosity']
        self.setup_permissions(verbosity=verbosity)

    def setup_permissions(self, **kwargs) -> None:
        """Get and set permissions for the groups that should have them."""
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Group, Permission
        verbosity = kwargs['verbosity']
        if verbosity >= 1:
            print('Setting up permissions for all user roles.')
        Review = self.get_model('Review')
        Comment = self.get_model('Comment')
        review_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Review))
        comment_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Comment))
        Group.objects.get_or_create(name='user')
        moderators, created = Group.objects.get_or_create(name='moderator')
        if verbosity >= 2:
            print('Setting up moderator permissions.')
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
        if verbosity >= 2:
            print('Setting up administrator permissions.')
        admins.permissions.set(Permission.objects.all())

    def prepopulate_database(self, verbosity) -> None:
        """Fill database with data from included csv files."""
        from django.contrib.auth.models import Group

        if verbosity >= 1:
            print('Populating database with test data.')
        User = get_user_model()
        Genre = self.get_model('Genre')
        Category = self.get_model('Category')
        Title = self.get_model('Title')
        Review = self.get_model('Review')
        Comment = self.get_model('Comment')

        Group.objects.get_or_create(name='user')
        Group.objects.get_or_create(name='moderator')
        Group.objects.get_or_create(name='admin')

        user_data = get_csv_data(source='users')
        for payload in user_data:
            User.objects.get_or_create(**payload)

        for model in (Genre, Category):
            data = get_csv_data(source=model._meta.model_name)
            for payload in data:
                model.objects.get_or_create(**payload)

        title_data = get_csv_data(source='titles')
        for payload in title_data:
            set_by_id(payload, 'category')
            Title.objects.get_or_create(**payload)

        review_data = get_csv_data(source=Review._meta.model_name)
        for payload in review_data:
            set_by_id(payload, 'author')
            if not Review.objects.filter(id=payload['id']).exists():
                Review.objects.create(**payload)

        comment_data = get_csv_data(source='comments')
        for payload in comment_data:
            set_by_id(payload, 'author')
            if not Comment.objects.filter(id=payload['id']).exists():
                Comment.objects.create(**payload)

    def ready(self) -> None:
        post_migrate.connect(self.post_migration, sender=self)
