from ninja.errors import HttpError
from http import HTTPStatus as status


exceptions_case = {
    TypeError: status.BAD_REQUEST
}

class GenericExceptionHandlerController:

    @staticmethod
    def execute(ex):
        status_code = exceptions_case.get(type(ex))
        if status_code:
            raise HttpError(status_code=status_code, message="Failed Request")
