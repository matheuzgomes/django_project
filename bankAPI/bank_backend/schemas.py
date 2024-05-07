from ninja import ModelSchema, Schema
from bank_backend.models import UserAccount, UserInformations
from decimal import Decimal


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
            'id',
            'account_type',
            'available_amount',
            'locked_amount',
            'loan_amount',
            'user_id'
        )

class InserUserInformations(Schema):
    user_info: str
    user_password: str
    national_id: str


class EncodedUserSecret(Schema):
    user_info: str
    user_password:str


class InsertUserAccount(Schema):
    available_amount: float
    loan_amount: float = None
    locked_amount: float = None

class UpdateUserAccount(Schema):
    available_amount: Decimal = None
    loan_amount: Decimal = None
    locked_amount: Decimal = None

