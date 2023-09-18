from rest_framework.test import APITestCase
from django.core.files.images import ImageFile

from entertainments.serializers import *
from entertainments.models import *


class NearestAPITestCase(APITestCase):

    def setUp(self):
        self.nearest_1 = NearestPlace.objects.create(
            title='test nearest 1',
            description='test description',
            location='test location'
        )
        self.nearest_2 = NearestPlace.objects.create(
            title='test nearest 2',
            description='test description',
            location='test location'
        )
        self.photo_1 = PhotoNearestPlace.objects.create(
            file=ImageFile(open("tests_media/mesye.png", "rb")),
            places=self.nearest_1
        )

    def test_get(self):
        url = 'http://127.0.0.1:8000/api/nearests/'
        response = self.client.get(url)
        phoros_list = response.data[0]['photos']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(phoros_list[0])