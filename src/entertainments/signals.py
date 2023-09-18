import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from entertainments.models import PhotoEntertainment, PhotoGalery, PhotoNearestPlace


@receiver(signal=post_delete, sender=PhotoEntertainment, dispatch_uid='delete_entertainment_photo')
def delete_entertainment_photo(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)

    
@receiver(signal=post_delete, sender=PhotoGalery, dispatch_uid='delete_galery_photo')
def delete_galery_photo(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


@receiver(signal=post_delete, sender=PhotoNearestPlace, dispatch_uid='delete_nearests_photo')
def delete_nearests_photo(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)