from django.shortcuts import get_object_or_404
from ..models import UserInformations, UserAccount
from ninja import Router
from ..authentication_handler import AuthBearer
from ..schemas import (
    UserInformationsSchema,
    UserAccountSchema,
    InserUserInformationsSchema,
    InsertUserAccountSchema,
    UpdateUserAccountSchema,
)
from ..authentication_handler.authentication_handler import Authentication
from ..exception_handler import GenericExceptionHandlerController


router = Router()


class BankApi:
    @router.get("v1/accounts", response=list[UserAccountSchema], auth=AuthBearer())
    def get_accounts(request) -> list[UserAccount]:
        return UserAccount.objects.all().filter(user_id=request.auth["data"]["user_id"])

    @router.get("v1/users", response=list[UserInformationsSchema], auth=AuthBearer())
    def get_users(request) -> list[UserInformations]:
        return UserInformations.objects.all()

    @router.post("v1/users/create", response=UserInformationsSchema)
    def create_user(request, item: InserUserInformationsSchema) -> UserInformations:
        encoded_password = Authentication.hash_password(
            {"user_password": item.user_password}
        )

        inserted_model = UserInformations.objects.create(
            user_info=item.user_info.strip(),
            user_password=encoded_password,
            national_id=item.national_id.strip(),
        )

        return inserted_model

    @router.post(
        "v1/users/create/account", response=UserAccountSchema, auth=AuthBearer()
    )
    def create_user_account(request, item: InsertUserAccountSchema) -> UserAccount:
        inserted_model = UserAccount.objects.create(
            available_amount=item.available_amount,
            locked_amount=item.locked_amount,
            loan_amount=item.loan_amount,
            user_id=UserInformations(**request.auth["data"]),
        )

        return inserted_model

    @router.put("v1/users/update/account/{account_id}", auth=AuthBearer())
    def update_user_account(
        request, account_id: int, item: UpdateUserAccountSchema
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

    @router.delete("v1/users/delete/account/{account_id}", auth=AuthBearer())
    def delete_user_account(request, account_id: int) -> dict[str, bool]:
        get_account = get_object_or_404(
            UserAccount, id=account_id, user_id=request.auth["data"]["user_id"]
        )

        get_account.delete()

        return {"success": True}

    @router.put("v1/users/lock/amount/{account_id}", auth=AuthBearer())
    def lock_user_amount(
        request, account_id: int, data: UpdateUserAccountSchema
    ) -> dict[str, bool]:
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
            "locked_amount": get_account.locked_amount,
        }

        return serialize
