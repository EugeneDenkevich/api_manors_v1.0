from decimal import Decimal

from django.contrib.admin.sites import DefaultAdminSite
from django.test import RequestFactory, TestCase
from authentication.models import BaseUser

from object.admin import *
from object.models import *
from object.logic import *


class ObjectFeatureTestCase(TestCase):

    def test_add_feature(self):
        object_1 = Object.objects.create(title='Title1',
                                         pers_num=5,
                                         description_short='Description',
                                         description_long='DescriptionDescriptionDescription',
                                         price_weekday=Decimal('120'),
                                         price_holiday=Decimal('220'),
                                         created_date='2023-05-01',
                                         is_reserved=False)
        ObjectFeature.objects.create(type='Shower', object_id=object_1)
        ObjectFeature.objects.create(type='Shower', object_id=object_1)

        self.assertEqual(len(object_1.features.all()), 1)


class PurchaseTestCase(TestCase):

    def setUp(self):
        self.object_1 = Object.objects.create(title='Title1',
                                              pers_num=5,
                                              description_short='Description',
                                              description_long='DescriptionDescriptionDescription',
                                              price_weekday=Decimal('120'),
                                              price_holiday=Decimal('220'),
                                              created_date='2023-05-01',
                                              is_reserved=False)
        self.object_2 = Object.objects.create(title='Title1',
                                              pers_num=5,
                                              description_short='Description',
                                              description_long='DescriptionDescriptionDescription',
                                              price_weekday=Decimal('120'),
                                              price_holiday=Decimal('220'),
                                              created_date='2023-05-01',
                                              is_reserved=False)
        self.purchase_1 = Purchase.objects.create(fio='Eugene',
                                                sex="m",
                                                passport_country='Беларусь',
                                                address='21 Судиловского',
                                                phone_number="+375336680390",
                                                email="eugenestudio@mail.ru",
                                                telegram="@eugenvazgen",
                                                object=self.object_1,
                                                count_adult=2,
                                                count_kids=1,
                                                desired_arrival="2023-06-05",
                                                desired_departure="2023-06-16",
                                                pets='',
                                                comment='123')

        self.user = BaseUser()

    def test_is_object_reserved_true(self):
        data = {
            'fio': 'Eugene',
            'sex': "Мужской",
            'passport_country': 'Беларусь',
            'address': '21 Судиловского',
            'phone_number': "+375336680390",
            'email': "eugenestudio@mail.ru",
            'telegram': "@eugenvazgen",
            'object': self.object_2,
            'desired_arrival': "2023-06-05",
            'desired_departure': "2023-06-16",
            'count_adult':2,
            'count_kids':2,
        }
        form = PurchaseAdminObjectFrom(data=data)
        self.assertTrue(form.is_valid())
    
    def test_is_object_reserved_false(self):
        data = {
            'fio': 'Eugene',
            'sex': "m",
            'passport_country': 'Беларусь',
            'address': '21 Судиловского',
            'phone_number': "+375336680390",
            'email': "eugenestudio@mail.ru",
            'telegram': "@eugenvazgen",
            'object': self.object_1,
            'desired_arrival': "2023-06-05",
            'desired_departure': "2023-06-16"
        }
        form = PurchaseAdminObjectFrom(data=data)
        self.assertFalse(form.is_valid())

    def test_check_departure_date(self):
        data = {
            "object": self.object_1.pk,
            "fio": "string",
            "sex": "Мужской",
            "passport_country": "string",
            "address": "string",
            "phone_number": "+375336680390",
            "email": "user@example.com",
            "telegram": "string",
            "desired_arrival": "2023-08-25",
            "desired_departure": "2023-08-24",
            "stat": "New",
            "count_adult": 20,
            "count_kids": 20,
            "pets": "string",
            "comment": "string"
        }
        form = PurchaseAdminObjectFrom(data=data)
        expected_report = {'desired_departure': [ValidationError(['Дата выезда должна быть раньше даты заезда'])]}
        self.assertEqual(str(form.errors.as_data()), str(expected_report))
