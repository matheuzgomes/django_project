from ninja import Schema


class InserUserInformationsSchema(Schema):
    user_info: str
    user_password: str
    national_id: str