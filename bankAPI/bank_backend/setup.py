from ninja import NinjaAPI
from .controlllers.bank_transactions import router as transaction_router
from .controlllers.user_utilities import router as user_router
class Setup:

    @staticmethod
    def return_setup(api:NinjaAPI):
        return api

api = Setup.return_setup(NinjaAPI())


api.add_router("/bank/", transaction_router)
api.add_router("/user/", user_router)

