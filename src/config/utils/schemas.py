from dataclasses import dataclass
from typing import Dict, List

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


@dataclass
class BasicAPISchema:
    tags: List
    success_200: List | None = None

    def __post_init__(self):
        self.statuses = {
            200: self.get_204(),
            400: self.get_400(),
            401: self.get_401(),
            403: self.get_403(),
            404: self.get_404(),
            500: self.get_500(),
        }

    def retrieve(self):
        pass

    def list(self):
        pass

    def create(self):
        pass

    def partial_update(self):
        pass

    def destroy(self):
        pass

    def post(self):
        pass

    def extend_schema(self, *args, **kwargs):
        return extend_schema(tags=self.tags, examples=self.success_200, *args, **kwargs)
    
    def get_responses(self, *statuses) -> Dict:
        responses = {}
        for status in statuses:
            responses.update(self.statuses[status]) if status in self.statuses else {}
        return responses

    @staticmethod
    def get_204() -> Dict:
        return {
            204: 'No content'
        }

    @staticmethod
    def get_400() -> Dict:
        return {
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Bed Request",
                        description='Bad Request',
                        value={"detail": "Страница не найдена."},
                        response_only=True,
                    ),
                ]
            )
        }
    
    @staticmethod
    def get_401() -> Dict:
        return {
            401: 'Unauthorized'
        }
    
    @staticmethod
    def get_403() -> Dict:
        return {
            403: 'Forbidden'
        }
    
    @staticmethod
    def get_404() -> Dict:
        return {
            404: OpenApiResponse(
                    response=OpenApiTypes.OBJECT,
                    examples=[OpenApiExample(
                             "Not Found",
                             description='Not Found',
                             value={"detail": "Страница не найдена."},
                             response_only=True,
                             ),]
                )
        }

    @staticmethod
    def get_500() -> Dict:
        return {
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Internal Server Error",
                        description='Internal Server Error',
                        value={"detail": "Ошибка сервера."},
                        response_only=True,
                    ),
                ]
            )
        }