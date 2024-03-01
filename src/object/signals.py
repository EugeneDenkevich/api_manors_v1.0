import os
import logging

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from object.models import PhotoObject
from object.models import Purchase
from bot import bot_service


@receiver(signal=post_delete, sender=PhotoObject, dispatch_uid='delete_object_photo')
def delete_object_photo(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


@receiver(signal=pre_save, sender=Purchase, dispatch_uid='save_purchase')
def create_message_for_bot(sender, instance: Purchase, **kwargs):
    message = f"Новый заказ #{instance.pk}:\n" \
              f"Заселение: {instance.desired_arrival}\n" \
              f"Выселение: {instance.desired_departure}\n" \
              f"Почта: {instance.email}\n"
    logging.info("MESSAGE WAS SENT: %s".format(message))
    bot_service.send_message(chat_id=5508567586, message=message)
