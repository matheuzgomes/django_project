from ninja import ModelSchema
from bank_backend.models import UserAccount
from .user_information_schema import UserInformationsSchema


class UserAccountSchema(ModelSchema):

    user_id : UserInformationsSchema

    class Meta:
        model = UserAccount
        fields = (
            'id',
            'account_type',
            'available_amount',
            'locked_amount',
            'loan_amount',
            'user_id'
        )