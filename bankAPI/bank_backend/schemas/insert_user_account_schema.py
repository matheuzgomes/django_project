from ninja import Schema


class InsertUserAccountSchema(Schema):
    available_amount: float
    loan_amount: float = None
    locked_amount: float = None