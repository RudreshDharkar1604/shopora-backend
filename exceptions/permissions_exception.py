from exceptions.base_excpetion import BaseException

class InvalidAccessException(BaseException):
    def __init__(self, user_role, message = None):
        super().__init__(status_code=404, details=f"{user_role} don't have permission to access this route !", message="Invalid Access !")