from decimal import Decimal
from ninja import Schema


class UpdateUserAccountSchema(Schema):
    available_amount: Decimal = None
    loan_amount: Decimal = None
    locked_amount: Decimal = None