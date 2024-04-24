from ninja import NinjaAPI
from .models import UserInformations, UserAccount
from .schemas import UserInformationsSchema, UserAccountSchema

class Setup:

    @staticmethod
    def return_setup(api:NinjaAPI):
        return api

api = Setup.return_setup(NinjaAPI())


@api.get("v1/bank/accounts", response=list[UserAccountSchema])
def get_accounts(request):
    return UserAccount.objects.all()


@api.get("v1/bank/users", response=list[UserInformationsSchema])
def get_users(request):
    return UserInformations.objects.all()