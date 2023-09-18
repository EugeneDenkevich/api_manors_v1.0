from config.utils.schemas import BasicAPISchema

from .serializers import (
    MainPageModelSerializer,
    BackPhotoSerializer,
    PolicyAgreementsSerializer,
)


class MainPageSchema(BasicAPISchema):
    def list(self):
        return self.extend_schema(
            summary='Get main page',
            description='Get main page',
            request=MainPageModelSerializer,
            responses={
                200: MainPageModelSerializer,
                **self.get_responses(404)
            }
        )
    

class BackPhotoSchema(BasicAPISchema):
    def list(self):
        return self.extend_schema(
            summary='Get background photos',
            description='Get background photos',
            request=BackPhotoSerializer,
            responses={
                200: BackPhotoSerializer,
                **self.get_responses(404)
            }
        )
    

class PolicyAgreementSchema(BasicAPISchema):
    def list(self):
        return self.extend_schema(
            summary='Get Policy and Agreement',
            description='Get Policy and Agreement',
            request=PolicyAgreementsSerializer,
            responses={
                200: PolicyAgreementsSerializer,
                **self.get_responses(404)
            }
        )


main_page_schema = MainPageSchema(tags=['Main page'])
back_photos_schema = BackPhotoSchema(tags=['Background photos'])
policy_agreement_schema = PolicyAgreementSchema(tags=['Policy and Agreement'])