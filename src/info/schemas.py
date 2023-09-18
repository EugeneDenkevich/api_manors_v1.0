from config.utils.schemas import BasicAPISchema
from drf_spectacular.utils import OpenApiExample

from . import serializers

  
class InfoSchema(BasicAPISchema):
    def list(self):
        return self.extend_schema(
            summary='Get info',
            description='Get info',
            request=serializers.InfoSerializer,
            responses={
                200: serializers.InfoSerializer,
            }
        )


class DishSchema(BasicAPISchema):
    def list(self):
        return self.extend_schema(
            description='Get dishes',
            summary='Get dishes',
            request=serializers.DishSerializer,
            responses={
                200: serializers.DishSerializer,
            }
        )


class MealSchema(BasicAPISchema):
    def list(self):
        return self.extend_schema(
            summary='Get meals',
            description='Get meals',
            request=serializers.MealInfoSerializer,
            responses={
                200: serializers.MealInfoSerializer,
            }
        )

class RuleSchema(BasicAPISchema):
    def list(self):
        return self.extend_schema(
            summary='Get rules',
            description='Get rules',
            request=serializers.RuleSerializer,
            responses={
                200: serializers.RuleSerializer,
            }
        )


info_schema = InfoSchema(tags=['Info'])
dish_schema = DishSchema(tags=['Dish'])
feeding_info_schema = MealSchema(tags=['Meals'])
rule_schema = RuleSchema(tags=['Rule'])