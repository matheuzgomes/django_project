from ninja import ModelSchema
from bank_backend.models import UserInformations


class UserInformationsSchema(ModelSchema):

    class Meta:
        model = UserInformations
        fields = (
            'user_id',
            'user_info',
            'national_id'
        )
