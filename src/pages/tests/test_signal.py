import os

from django.test import TestCase
from django.core.files.images import ImageFile

from pages import models


class PhotoMainPageTestCase(TestCase):

    def setUp(self):
        self.main_page_1 = models.MainPage.objects.create(
            title='test',
            house_title='test',
            entertainment_title='test',
        )
        self.photo_main_page_1 = models.PhotoMainPage.objects.create(
            file=ImageFile(open('tests_media/mesye.png', 'rb')),
            main_page=self.main_page_1
        )

    def test_if_photo_file_was_deleted_after_deleting_photo_object(self):
        self.assertEqual(os.path.exists(self.photo_main_page_1.file.path), True)
        self.photo_main_page_1.delete()
        self.assertEqual(os.path.exists(self.photo_main_page_1.file.path), False)


class BackPhotoTestCase(TestCase):

    def setUp(self):
        self.back_photo_1 = models.BackPhoto.objects.create(
            photo_m=ImageFile(open('tests_media/mesye.png', 'rb')),
            photo_h=ImageFile(open('tests_media/mesye.png', 'rb')),
            photo_k=ImageFile(open('tests_media/mesye.png', 'rb')),
            photo_e=ImageFile(open('tests_media/mesye.png', 'rb')),
        )

    def check_photo_changing(self, *args):
        for photo_x in args:
            field_name = photo_x.field.name
            old_path = photo_x.path
            self.assertEqual(os.path.exists(old_path), True)
            setattr(self.back_photo_1, field_name, ImageFile(open('tests_media/mesye2.png', 'rb')))
            self.back_photo_1.save()
            self.assertEqual(os.path.exists(old_path), False)
            new_path = getattr(self.back_photo_1, field_name).path
            self.assertEqual(os.path.exists(new_path), True)
        

    def test_check_if_photo_deletes_after_changing_object_or_deleting(self):
        self.check_photo_changing(self.back_photo_1.photo_m,
                                   self.back_photo_1.photo_h,
                                   self.back_photo_1.photo_k,
                                   self.back_photo_1.photo_e)
        self.back_photo_1.delete()
        self.assertEqual((os.path.exists(self.back_photo_1.photo_h.path) or
                          os.path.exists(self.back_photo_1.photo_m.path) or
                          os.path.exists(self.back_photo_1.photo_k.path) or
                          os.path.exists(self.back_photo_1.photo_e.path)), False)

