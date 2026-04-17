from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import AppUser, Profile, Screenshot


@receiver(post_save, sender=AppUser)
def create_user_profile(sender, instance, created, **kwargs):
    # signal which will assign user to 'Regular Users' group and create a profile when appuser is created
    if created:
        Profile.objects.create(user=instance)

        try:
            regular_users_group = Group.objects.get(name='Regular Users')
            instance.groups.add(regular_users_group)
        except Group.DoesNotExist:
            pass  # use management command `python manage.py create_user_groups` to create the group(s)


@receiver(post_save, sender=AppUser)
def save_user_profile(sender, instance, **kwargs):
    # signal to save the profile when the appuser is saved
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_delete, sender=Screenshot)
def decrement_screenshot_count_on_delete(sender, instance, **kwargs):
    # automatically decrement screenshot count when a screenshot is deleted
    if instance.uploaded_by and hasattr(instance.uploaded_by, 'profile'):
        instance.uploaded_by.profile.decrement_screenshots()
