from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from CheckPoint.saves.models import Save


@receiver(post_save, sender=Save, dispatch_uid="increment_saves_count")
def increment_saves_count_on_create(sender, instance, created, **kwargs):
    if created and instance.uploaded_by and hasattr(instance.uploaded_by, 'profile'):
        instance.uploaded_by.profile.increment_saves()


@receiver(post_delete, sender=Save, dispatch_uid="decrement_saves_count")
def decrement_saves_count_on_delete(sender, instance, **kwargs):
    if instance.uploaded_by and hasattr(instance.uploaded_by, 'profile'):
        instance.uploaded_by.profile.decrement_saves()

