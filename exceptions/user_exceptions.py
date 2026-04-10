from exceptions.base_excpetion import BaseException

class UserNotFoundException(BaseException):
    def __init__(self, userDetails, search_area=None):
        super().__init__(
            status_code=404, message=f"User not found ",
            details=f"User with details : {userDetails} not found in {search_area} "
        )


class UserAlreadyExists(BaseException):
    def __init__(self, userId):
        super().__init__(status_code=400, details=f"User with {userId} ID already exists ")