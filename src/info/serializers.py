from rest_framework.serializers import (
    CharField,
    ListSerializer,
    ModelSerializer,
    ChoiceField,
    URLField,
)

from .models import (
    CURRENCIES,
    Meal,
    Dish,
    Rule,
    Info,
    InfoSocial,
)


class PhonesListSerializer(ListSerializer):
    child = CharField()

    def to_representation(self, data):
        res = data.instance.phones.all()
        phone_numbers = list(map(lambda phone_object: 
                                 str(phone_object.phone), res))
        return phone_numbers


class SocialSerializer(ModelSerializer):
    social_type = URLField(required=False)

    class Meta:
        model = InfoSocial
        fields = ['social_type']

    def to_representation(self, instance):
        return instance


class InfoSerializer(ModelSerializer):
    social = SocialSerializer(many=True, required=False)
    phones = PhonesListSerializer(required=False)
    currency = ChoiceField(choices=CURRENCIES)
    
    class Meta:
        model = Info
        fields = '__all__'


class MealInfoSerializer(ModelSerializer):
    class Meta:
        model = Meal
        exclude = ['feeding']


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        exclude = ['feeding']


class RuleSerializer(ModelSerializer):
    class Meta:
        model = Rule
        exclude = ['rules', 'created_at', 'id']
