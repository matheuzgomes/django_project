from .setup import api
from .models import UserInformations, UserAccount
from .schemas import UserInformationsSchema, UserAccountSchema, InserUserInformations, EncodedUserSecret, InsertUserAccount
from .authentication import Authentication
from ninja.security import HttpBearer
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404

class AuthBearer(HttpBearer):

    def authenticate(self, request, credentials):
        token = Authentication().decode_token(token=credentials)

        BankApi.user_login(
            item=EncodedUserSecret(
                user_info = token['data']['user_info'],
                user_password = token['data']['user_password']
                ))

        return token

class BankApi:

    @api.get("v1/bank/accounts", response=list[UserAccountSchema], auth=AuthBearer())
    def get_accounts(request):
        return UserAccount.objects.all().filter(user_id = request.auth['data']['user_id'])

    @api.get("v1/bank/users", response=list[UserInformationsSchema], auth=AuthBearer())
    def get_users(request):
        return UserInformations.objects.all()

    @api.post("v1/bank/users/create", response=UserInformationsSchema)
    def create_user(request, item: InserUserInformations):


        encoded_password = Authentication.hash_password(
            {
                "user_password": item.user_password
            }
        )

        inserted_model = UserInformations.objects.create(
            user_info = item.user_info,
            user_password = encoded_password,
            national_id = item.national_id
            )

        return inserted_model

    @api.post("v1/bank/users/create/account", response=UserAccountSchema, auth=AuthBearer())
    def create_user_account(request, item: InsertUserAccount):

        inserted_model = UserAccount.objects.create(
            available_amount = item.available_amount,
            locked_amount = item.locked_amount,
            loan_amount = item.loan_amount,
            user_id = UserInformations(**request.auth['data'])
            )

        return inserted_model

    @api.post("v1/bank/users/login", response=str)
    def user_login(item: EncodedUserSecret, request = None):

        get_user = get_object_or_404(UserInformations, user_info = item.user_info)

        validation = Authentication.validate_user_password(item.user_password, get_user)

        if (validation is False):
            raise HttpError(
                401,
                'Invalid User'
            )

        return Authentication.create_access_token( 
            {
                "user_id": str(get_user.user_id),
                "user_info": item.user_info,
                "user_password": item.user_password,
            })

