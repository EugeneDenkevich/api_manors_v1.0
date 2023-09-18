import os

from django.db.models.signals import post_delete, pre_save, post_init
from django.dispatch import receiver

from info.models import Dish


@receiver(signal=post_delete, sender=Dish, dispatch_uid='delete_dish_photo')
def delete_dish_photo(sender, instance, **kwargs):
    if os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)

@receiver(signal=post_init, sender=Dish, dispatch_uid='init_origin_photo_dish')
def init_origin_photo_dish(sender, instance, **kwargs):
    if instance.photo:
        instance.origin_photo = instance.photo


@receiver(signal=pre_save, sender=Dish, dispatch_uid='delete_dish_photo_when_changed')
def delete_dish_photo_when_changed(sender, instance, **kwargs):
    if (hasattr(instance, 'origin_photo') and os.path.isfile(instance.origin_photo.path) and
        instance.origin_photo.path != instance.photo.path):
        os.remove(instance.origin_photo.path)