from ninja import Schema


class EncodedUserSecretSchema(Schema):
    user_info: str
    user_password:str