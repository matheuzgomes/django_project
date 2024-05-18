from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from .setup import api
from .authentication_handler import AuthBearer
from .models import UserInformations, UserAccount
from .schemas import (
    UserInformationsSchema,
    UserAccountSchema,
    InserUserInformations,
    EncodedUserSecret,
    InsertUserAccount,
    UpdateUserAccount,
)
from .authentication_handler.authentication_handler import Authentication
from .exception_handler import GenericExceptionHandlerController


class BankApi:
    @api.get("v1/bank/accounts", response=list[UserAccountSchema], auth=AuthBearer())
    def get_accounts(request) -> list[UserAccount]:
        return UserAccount.objects.all().filter(user_id=request.auth["data"]["user_id"])

    @api.get("v1/bank/users", response=list[UserInformationsSchema], auth=AuthBearer())
    def get_users(request) -> list[UserInformations]:
        return UserInformations.objects.all()

    @api.post("v1/bank/users/create", response=UserInformationsSchema)
    def create_user(request, item: InserUserInformations) -> UserInformations:
        encoded_password = Authentication.hash_password(
            {"user_password": item.user_password}
        )

        inserted_model = UserInformations.objects.create(
            user_info=item.user_info.strip(),
            user_password=encoded_password,
            national_id=item.national_id.strip(),
        )

        return inserted_model

    @api.post("v1/bank/users/create/account", response=UserAccountSchema, auth=AuthBearer())
    def create_user_account(request, item: InsertUserAccount) -> UserAccount:
        inserted_model = UserAccount.objects.create(
            available_amount=item.available_amount,
            locked_amount=item.locked_amount,
            loan_amount=item.loan_amount,
            user_id=UserInformations(**request.auth["data"]),
        )

        return inserted_model

    @api.post("v1/bank/users/login", response=str)
    def user_login(request, item: EncodedUserSecret) -> str:
        get_user = get_object_or_404(UserInformations, user_info=item.user_info)

        validation = Authentication.validate_user_password(item.user_password, get_user)

        if validation is False:
            raise HttpError(401, "Invalid User")

        return Authentication.create_access_token(
            {
                "user_id": str(get_user.user_id),
                "user_info": item.user_info,
                "user_password": item.user_password,
            }
        )

    @api.put("v1/bank/users/update/account/{account_id}", auth=AuthBearer())
    def update_user_account(
        request, account_id: int, item: UpdateUserAccount
    ) -> dict[str, bool]:
        account_for_update = get_object_or_404(
            UserAccount, id=account_id, user_id=request.auth["data"]["user_id"]
        )

        account_for_update.available_amount = item.available_amount
        account_for_update.loan_amount = (
            item.loan_amount
            if item.loan_amount is not None
            else account_for_update.loan_amount
        )
        account_for_update.locked_amount = (
            item.locked_amount
            if item.locked_amount is not None
            else account_for_update.locked_amount
        )

        account_for_update.save()

        return {"success": True}

    @api.delete("v1/bank/users/delete/account/{account_id}", auth=AuthBearer())
    def delete_user_account(request, account_id: int) -> dict[str, bool]:
        get_account = get_object_or_404(
            UserAccount, id=account_id, user_id=request.auth["data"]["user_id"]
        )

        get_account.delete()

        return {"success": True}

    @api.put("v1/bank/users/lock/amount/{account_id}", auth=AuthBearer())
    def lock_user_amount(request, account_id: int, data: UpdateUserAccount) -> dict[str, bool]:

        get_account = get_object_or_404(
            UserAccount, id=account_id, user_id=request.auth["data"]["user_id"]
        )
        try:
            if get_account.available_amount > 0:
                get_account.locked_amount += data.locked_amount
                get_account.available_amount -= data.locked_amount

                get_account.save()

        except Exception as e:
            GenericExceptionHandlerController.execute(e)

        
        serialize = {
            "available_amount": get_account.available_amount,
            "loan_amount": get_account.loan_amount,
            "id": get_account.id,
            "locked_amount": get_account.locked_amount
        }

        return serialize
