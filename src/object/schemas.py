from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from config.utils.schemas import BasicAPISchema

from .serializers import (
    ObjectSerializer,
    PurchaseSerializer
)


class ObjectSchema(BasicAPISchema):

    def retrieve(self):
        return self.extend_schema(
            description='Get house by id',
            summary='Get house by id',
            request=ObjectSerializer,
            responses={
                200: ObjectSerializer,
                **self.get_responses(404)
            }
        )

    def list(self):
        return self.extend_schema(
            description='Get all houses aaa bbb ccc',
            summary='Get all houses',
            request=ObjectSerializer,
            responses={
                200: ObjectSerializer,
                **self.get_responses(404)
            }
        )


class PurchaseSchema(BasicAPISchema):

    API_ERRORS = {
        'detail:Have some mistakes in JSON syntax.':
                        'JSON parse error - <explanation_string>: line <int> column <int> (char <int>).',
        'required_field_name:The required_field_name key will be replaced by the name of required field which wasn\'t filled in.':
                        ['Обязательное поле.'],
        'object:You probably pointed a not-existent house id,':
                        ['Недопустимый первичный ключ \"0\" - объект не существует.'],
        'fio:You have exceeded the maximum number of characters in string (300).:':
                        ['Убедитесь, что это значение содержит не более 300 символов.'],
        'sex:Use only forllowing variants - [\'Мужской\', \'Женский\'].':
                        ['Значения <string> нет среди допустимых вариантов.'],
        'passport_country:You have exceeded the maximum number of characters in string (256.)':
                        ['Убедитесь, что это значение содержит не более 256 символов.'],
        'phone_number:You have exceeded the maximum number of characters in string (256).':
                        ['Убедитесь, что это значение содержит не более 256 символов.'],
        'email:Use the correct email address, like user@user.ru.':
                        ['Введите правильный адрес электронной почты.'],
        'telegram:You have exceeded the maximum number of characters in string (256).':
                        ['Убедитесь, что это значение содержит не более 256 символов.'],
        'desired_arrival:Use the correct data format, like 2023-01-01.':
                        ['Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD.'],
        'desired_departure:1. Use the correct data format, like 2023-01-01.\n\n'
                          '2. Check if you entered the correct departure date. It has to be later than arrival date.':
                        ['Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD.',
                         'The departure date should be later than the arrival date.'],
        'count_adult:Enter the integer value between 0 and 20':
                        ['Убедитесь, что это значение меньше либо равно 20.',
                         'Убедитесь, что это значение больше либо равно 0.'],
        'count_kids:Enter the integer value between 0 and 20':
                        ['Убедитесь, что это значение меньше либо равно 20.',
                         'Убедитесь, что это значение больше либо равно 0.'],
    }
    
    BAD_REQUEST_400 = [
        OpenApiExample(
            name=k.split(':')[0],
            response_only=True,
            value={k.split(':')[0]: v},
            description=k.split(':')[1])
        for k, v in API_ERRORS.items()
    ]

    def create(self):
        return self.extend_schema(
                    description='Create purchase',
                    summary='Create purchase',
                    request=PurchaseSerializer,
                    responses={
                        201: PurchaseSerializer,
                        400: OpenApiResponse(response='response',
                                            description='Description of Status Code 400 cases',
                                            examples=self.BAD_REQUEST_400)
                    },
                )


house_schema = ObjectSchema(tags=['Houses'])
purchase_schema = PurchaseSchema(tags=['Purchase'])