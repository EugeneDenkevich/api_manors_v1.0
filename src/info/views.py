from rest_framework.viewsets import mixins, GenericViewSet
from django.utils.decorators import method_decorator

from .schemas import *
from .models import *
from .serializers import *

@method_decorator(name='list', decorator=info_schema.list())
class InfoModelViewSet(mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Info.objects.all().prefetch_related('socials')
    serializer_class = InfoSerializer


@method_decorator(name='list', decorator=dish_schema.list())
class DishModelViewSet(mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


@method_decorator(name='list', decorator=feeding_info_schema.list())
class MealModelViewSet(mixins.ListModelMixin,
                              GenericViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealInfoSerializer


@method_decorator(name='list', decorator=rule_schema.list())
class RuleModelViewSet(mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
