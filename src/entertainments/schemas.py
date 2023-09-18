from config.utils.schemas import BasicAPISchema

from .serializers import (
    EntertainmentSerializer,
)


class EntertainmentsSchema(BasicAPISchema):

    def retrieve(self):
        return self.extend_schema(
            description='Get entertainment by id',
            summary='Get entertainment by id',
            request=EntertainmentSerializer,
            responses={
                200: EntertainmentSerializer,
                **self.get_responses(404)
            }
        )

    def list(self):
        return self.extend_schema(
            description='Get entertainments',
            summary='Get entertainments',
            request=EntertainmentSerializer,
            responses={
                200: EntertainmentSerializer,
            }
        )
    

class GalerySchema(BasicAPISchema):
    
    def list(self):
        return self.extend_schema(
            summary='Get galeries',
            description='Get galeries',
        )
    

class NearestSchema(BasicAPISchema):
    
    def list(self):
        return self.extend_schema(
            summary='Get nearesrs',
            description='Get nearesrs',
        )


entertainment_schema = EntertainmentsSchema(tags=['Entertainment'])
galery_schema = GalerySchema(tags=['Galery'])
nearest_schema = NearestSchema(tags=['Nearests Places'])
