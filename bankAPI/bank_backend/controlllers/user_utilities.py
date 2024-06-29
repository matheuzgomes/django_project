from ninja.errors import HttpError
from ninja import Router
from django.shortcuts import get_object_or_404
from ..models import UserInformations
from ..schemas import InserUserInformationsSchema, UserInformationsSchema
from ..authentication_handler.authentication_handler import Authentication
from ..schemas import EncodedUserSecretSchema
from ..authentication_handler import AuthBearer

router = Router()


class UserApi:

    @router.get("v1/users", response=list[UserInformationsSchema], auth=AuthBearer())
    def get_users(request) -> list[UserInformations]:
        return UserInformations.objects.all()

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
