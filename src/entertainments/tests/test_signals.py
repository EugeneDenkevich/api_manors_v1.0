import os

from django.test import TestCase
from django.core.files.images import ImageFile

from entertainments import models


class PhotoEntertinmentTestCase(TestCase):
    
    def setUp(self):
        self.entertainment_1 = models.Entertainment.objects.create(
            title='test',
            description_short='test',
            description_long='test',
        )
        self.photo_entertainment_1 = models.PhotoEntertainment.objects.create(
            file=ImageFile(open('tests_media/mesye.png', 'rb')),
            entertainment=self.entertainment_1
        )
    
    def test_check_if_photo_file_was_deleted_after_photo_object_was_deleted(self):
        self.assertEqual(os.path.exists(self.photo_entertainment_1.file.path), True)
        self.photo_entertainment_1.delete()
        self.assertEqual(os.path.exists(self.photo_entertainment_1.file.path), False)


class PhotoNearestPlaceTestCase(TestCase):
    
    def setUp(self):
        self.nearest_1 = models.NearestPlace.objects.create(
            title='test',
            description='test',
            location='test',
        )
        self.photo_nearest_1 = models.PhotoNearestPlace.objects.create(
            file=ImageFile(open('tests_media/mesye.png', 'rb')),
            places=self.nearest_1
        )
    
    def test_check_if_photo_file_was_deleted_after_photo_object_was_deleted(self):
        self.assertEqual(os.path.exists(self.photo_nearest_1.file.path), True)
        self.photo_nearest_1.delete()
        self.assertEqual(os.path.exists(self.photo_nearest_1.file.path), False)


class PhotoGaleryTestCase(TestCase):
    
    def setUp(self):
        self.galery_1 = models.Galery.objects.create(
            title='test',
        )
        self.photo_galery_1 = models.PhotoGalery.objects.create(
            file=ImageFile(open('tests_media/mesye.png', 'rb')),
            galeries=self.galery_1
        )
    
    def test_check_if_photo_file_was_deleted_after_photo_object_was_deleted(self):
        self.assertEqual(os.path.exists(self.photo_galery_1.file.path), True)
        self.photo_galery_1.delete()
        self.assertEqual(os.path.exists(self.photo_galery_1.file.path), False)
