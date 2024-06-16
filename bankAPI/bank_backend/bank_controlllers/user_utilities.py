from ninja.errors import HttpError
from ninja import Router
from django.shortcuts import get_object_or_404
from ..models import UserInformations
from ..authentication_handler.authentication_handler import Authentication
from ..schemas import EncodedUserSecretSchema

router = Router()

class UserApi:

    @router.post("v1/login", response=str)
    def user_login(request, item: EncodedUserSecretSchema) -> str:
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
