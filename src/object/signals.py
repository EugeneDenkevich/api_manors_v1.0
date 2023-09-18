import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from object.models import PhotoObject


@receiver(signal=post_delete, sender=PhotoObject, dispatch_uid='delete_object_photo')
def delete_object_photo(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
