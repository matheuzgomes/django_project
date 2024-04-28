from ninja import NinjaAPI

class Setup:

    @staticmethod
    def return_setup(api:NinjaAPI):
        return api

api = Setup.return_setup(NinjaAPI())
