from ninja.security import HttpBearer
from ninja.errors import AuthenticationError
from ..controlllers.user_utilities import UserApi
from ..schemas import EncodedUserSecretSchema
from .authentication_handler import Authentication


class AuthBearer(HttpBearer):

    def __init__(self, user_api: UserApi = UserApi) -> None:
        self.user = user_api

    def authenticate(self, api, request):
        try:
            token = Authentication().decode_token(token=request)

            if token:

                self.user.user_login(
                    request,
                    item=EncodedUserSecretSchema(
                        user_info=token["data"]["user_info"],
                        user_password=token["data"]["user_password"],
                    ),
                )

                return token
        except Exception as e:
            raise AuthenticationError(f"Failed to authenticate : {str(e)}")

        return token
