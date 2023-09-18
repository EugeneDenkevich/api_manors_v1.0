from rest_framework.test import APITestCase
from rest_framework import status

from info.serializers import *
from info.models import *


class InfoAPITestCase(APITestCase):

    def setUp(self):
        info = Info.objects.create(
            address = 'King street - 9',
            comment = 'Funny comment',
            latitude = "string",
            longitude = "string",
            currency = "byn"
        )
        social_1 = InfoSocial.objects.create(
            type = 'Facebook',
            link = 'https://www.facebook.com',
            info = info
        )

    def test_get(self):
        url = 'http://127.0.0.1:8000/api/info/'
        response = self.client.get(url)
        info = Info.objects.all()
        serializer_data = InfoSerializer(info, many=True).data
        social = serializer_data[0]['social']
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(social, [{'Facebook': 'https://www.facebook.com'}])
        self.assertEqual(serializer_data, response.data)
