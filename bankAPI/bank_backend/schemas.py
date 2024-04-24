from ninja import ModelSchema
from bank_backend.models import UserAccount, UserInformations



class UserInformationsSchema(ModelSchema):

    class Meta:
        model = UserInformations
        fields = (
            'user_id',
            'user_info',
            'national_id'
        )

class UserAccountSchema(ModelSchema):

    user_id : UserInformationsSchema

    class Meta:
        model = UserAccount
        fields = (
            'available_amount',
            'locked_amount',
            'loan_amount',
            'user_id'
        )
