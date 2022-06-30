from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model

from reviews.utils import get_csv_data


class ReviewsConfig(AppConfig):
    name = 'reviews'
    verbose_name = name.capitalize()

    def prepopulate_database(self, sender, **kwargs) -> None:
        """fill database with data from included csv files"""

        from django.contrib.auth.models import Group
        User = get_user_model()
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

    def ready(self) -> None:

        post_migrate.connect(self.prepopulate_database, sender=self)
        return super().ready()
