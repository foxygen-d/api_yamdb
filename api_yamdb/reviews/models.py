from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission, AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models


#DjangoUser = get_user_model()


class User(AbstractUser):
    role = models.ManyToManyField(
        Group,
        through='Roles',
        null=False,
        blank=False,
    ),
    bio = models.TextField(
        'Biography',
        null=True,
        blank=True,
    )


class Roles(models.Model):
    class Meta:
        verbose_name_plural = 'User-Group Relations'

    group_name = models.OneToOneField(Group, to_field='name', primary_key=True, on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    pass


class Comment(models.Model):
    pass


# assigning permissions

moderators = Group.objects.get_or_create(name="Moderator")
admins = Group.objects.get_or_create(name="Admin")

review_ctp = ContentType.objects.get_for_model(Review)
print(review_ctp)

review_permissions = Permission.objects.filter(
    content_type=review_ctp)
comment_permissions = Permission.objects.filter(
    content_type=ContentType.objects.get_for_model(Comment))

moderator_permissions = (
    filter(lambda perm: perm.codename in ('delete_review', 'change_review'), review_permissions)
    + filter(lambda perm: perm.codename in ('delete_comment', 'change_comment'), comment_permissions)
)
moderators.permissions.add(*moderator_permissions)
admins.permissions.set(Permission.objects.all())