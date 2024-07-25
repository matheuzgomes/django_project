from ninja.errors import HttpError
from ninja import Router
from django.shortcuts import get_object_or_404
from ..models import UserInformations
from ..schemas import InserUserInformationsSchema, UserInformationsSchema
from ..utils.authentication_handler import AuthenticationHandler
from ..schemas import EncodedUserSecretSchema

router = Router()

class LoginController:

    @router.post("v1/login", response=str)
    def user_login(request, item: EncodedUserSecretSchema) -> str:
        get_user = get_object_or_404(UserInformations, user_info=item.user_info)

        validation = AuthenticationHandler.validate_user_password(item.user_password, get_user)

        if validation is False:
            raise HttpError(401, "Invalid User")

        return AuthenticationHandler.create_access_token(
            {   
                "user_id": str(get_user.user_id),
                "user_info": item.user_info,
                "user_password": item.user_password,
            }
        )

    @router.post("v1/users/create", response=UserInformationsSchema)
    def create_user(request, item: InserUserInformationsSchema) -> UserInformations:

        encoded_password = AuthenticationHandler.hash_password(
            {"user_password": item.user_password}
        )

        inserted_model = UserInformations.objects.create(
            user_info=item.user_info.strip(),
            user_password=encoded_password,
            national_id=item.national_id.strip(),
        )

        return inserted_model
