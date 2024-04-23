from ninja import ModelSchema
from .models import UserAccount, UserInfo



class UserInfoSchema(ModelSchema):
    class Meta:
        model = UserInfo
        fields = (
            'user_id',
            'user_info',
            'national_id',
            'user_account'
        )

class UserAccountSchema(ModelSchema):
    class Meta:
        model = UserAccount
        fields = (
            'available_amount',
            'locked_amount',
            
        )
