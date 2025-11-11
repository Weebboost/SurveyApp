class BaseException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class EmailAlreadyExistsException(BaseException):
    def __init__(self, message, status_code = 409):
        super().__init__(message, status_code)