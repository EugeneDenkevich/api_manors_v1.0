from drf_spectacular.utils import OpenApiResponse
from src.config.utils.schemas import BasicAPISchema
from drf_spectacular.types import OpenApiTypes
from .serializers import *


class TelegramSchema(BasicAPISchema):

    def retrieve(self):
        return self.extend_schema(
            description="Get owner by id",
            summary="Get owner by id",
            request=TelegramSerializer,
            responses={200: TelegramSerializer, **self.get_responses(404)},
        )

    def create(self):
        return self.extend_schema(
            description="Create owner",
            summary="Create owner",
            request=TelegramSerializer,
            responses={
                201: TelegramSerializer,
                400: OpenApiResponse(
                    response="response",
                    description="Description of Status Code 400 cases",
                ),
            },
        )

    def get_daily_data(self):
        return self.extend_schema(
            description='Get daily data',
            summary='Get daily data',
            responses={
                200: OpenApiResponse(
                        response=[OpenApiTypes.OBJECT],
                    ),
                **self.get_responses(500),
            },
        )


telegram_schema = TelegramSchema(tags=["Telegram"])
