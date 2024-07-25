from jwt import encode, decode, PyJWTError
from pydantic import ValidationError
from ninja.errors import HttpError
import os
from typing import Dict
from datetime import datetime, timedelta, timezone


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")


class AuthenticationHandler:
    @classmethod
    def create_access_token(cls, payload: Dict[str, str]):
        expiring_delta = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode = {"data": payload, "exp": expiring_delta}

        encoded_jwt = encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

        return encoded_jwt

    @classmethod
    def validate_user_password(self, password, hashed_info):
        try:
            payload = decode(hashed_info.user_password, JWT_SECRET_KEY, ALGORITHM)

            validate = payload["user_password"] == password

        except (PyJWTError, ValidationError) as e:
            raise HttpError(status_code=403, message="Could not validate credentials")
        return validate

    @classmethod
    def hash_password(cls, data: Dict[str, str]):
        try:
            hashed_password = encode(data, JWT_SECRET_KEY, ALGORITHM)

        except (PyJWTError, ValidationError) as e:
            raise HttpError(status_code=403, message="Could not validate credentials")

        return hashed_password

    @classmethod
    def decode_token(cls, token: str):
        try:
            decoded_token = decode(token, JWT_SECRET_KEY, ALGORITHM)

        except (PyJWTError, ValidationError) as e:
            raise HttpError(status_code=403, message="Could not validate credentials")

        return decoded_token
