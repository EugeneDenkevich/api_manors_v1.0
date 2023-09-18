import os

from django.test import TestCase
from django.core.files.images import ImageFile

from info import models


class SignalsTestCase(TestCase):
    
    def setUp(self) -> None:
        self.feeding_1 = models.FeedingInfo.objects.create()
        self.dish_1 = models.Dish.objects.create(
            title='test',
            description='test',
            photo=ImageFile(open('tests_media/mesye.png', 'rb')),
            feeding=self.feeding_1
        )

    def test_check_if_photo_exists_after_changing(self):
        old_path = self.dish_1.photo.path

        # Check if the old photo exists
        self.assertEqual(os.path.isfile(old_path), True)

        self.dish_1.photo = ImageFile(
            open('tests_media/mesye2.png', 'rb')
        )
        self.dish_1.save()

        # Check if the old photo was successfuly deleted after changing
        self.assertEqual(os.path.isfile(old_path), False)
        
        new_path = self.dish_1.photo.path

        # Check if the new photo was created after changing photo
        self.assertEqual(os.path.isfile(new_path), True)

        self.dish_1.delete()
        # Check if the new photo was successfuly deleted after deleting
        self.assertEqual(os.path.isfile(new_path), False)
