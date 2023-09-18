import os

from django.test import TestCase
from django.core.files.images import ImageFile

from object import models


class SignalsObjectTestCase(TestCase):
    
    def setUp(self):
        self.object = models.Object.objects.create(
            title='test',
            pers_num=1,
            description_short='test',
            description_long='test',
            price_weekday='200.00',
            price_holiday='200.00',
        )
        self.photo_1 = models.PhotoObject.objects.create(
            file=ImageFile('tests_media/mesye.png', 'rb'),
            object_id=self.object
        )

    def check_if_photo_deletes_if_after_photo_deleting(self):
        photo_path = self.photo_1.file.path
        self.assertEqual(os.path.exists(photo_path), True)
        self.photo_1.delete()
        self.assertEqual(os.path.exists(photo_path), False)
