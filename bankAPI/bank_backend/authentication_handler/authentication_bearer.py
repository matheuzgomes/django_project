from ninja.security import HttpBearer
from ..api import BankApi
from ..schemas import EncodedUserSecretSchema
from .authentication_handler import Authentication


class AuthBearer(HttpBearer):
    def authenticate(self, bank_api: BankApi, request, credentials):
        token = Authentication().decode_token(token=credentials)

        bank_api.user_login(
            request,
            item=EncodedUserSecretSchema(
                user_info=token["data"]["user_info"],
                user_password=token["data"]["user_password"],
            ),
        )

        return token
