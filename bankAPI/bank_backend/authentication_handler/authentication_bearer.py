from ninja.security import HttpBearer
from .authentication_handler import Authentication
from ..schemas import EncodedUserSecret
from ..api import BankApi


class AuthBearer(HttpBearer):
    def authenticate(self, bank_api: BankApi, request, credentials):
        token = Authentication().decode_token(token=credentials)

        bank_api.user_login(
            request,
            item=EncodedUserSecret(
                user_info=token["data"]["user_info"],
                user_password=token["data"]["user_password"],
            ),
        )

        return token
