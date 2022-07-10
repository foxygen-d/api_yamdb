# from django.apps import apps
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver


# @receiver(post_migrate)
# def setup_permissions(sender, **kwargs) -> None:
#     """Get and set permissions for the groups that should have them."""
#     verbosity = kwargs.get('verbosity') or 1
#     from django.contrib.contenttypes.models import ContentType
#     from django.contrib.auth.models import Group, Permission
#     if verbosity >= 1:
#         print("Setting up permissions for all user roles.")
#     Review = apps.get_model('reviews', 'Review')
#     Comment = apps.get_model('reviews', 'Comment')
#     # get all auto-generated permissions for Review and Comment models
#     review_permissions = Permission.objects.filter(
#         content_type=ContentType.objects.get_for_model(Review))
#     comment_permissions = Permission.objects.filter(
#         content_type=ContentType.objects.get_for_model(Comment))
#     # create new groups if DoesNotExist and assign respective permissions
#     Group.objects.get_or_create(name='user')
#     moderators, created = Group.objects.get_or_create(name="moderator")
#     admins, created = Group.objects.get_or_create(name="admin")
#     if not created:
#         if verbosity >= 2:
#             print('Setting up moderator permissions.')
#         moderator_permissions = (
#             list(filter(
#                 lambda perm: perm.codename in (
#                     'delete_review',
#                     'change_review'),
#                 review_permissions))
#             + list(filter(
#                 lambda perm: perm.codename in (
#                     'delete_comment',
#                     'change_comment'),
#                 comment_permissions))
#         )
#         moderators.permissions.add(*moderator_permissions)
#     if not created:
#         if verbosity >= 2:
#             print('Setting up administrator permissions.')
#         admins.permissions.set(Permission.objects.all())
#     if verbosity == 3:
#         print(f'Admins: {moderators.permissions.all()}')
#         print(f'Mods: {admins.permissions.all()}')
