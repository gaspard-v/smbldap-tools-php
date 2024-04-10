from typing import Optional
from ..utils.logger import log


class WrongPasswordException(Exception):
    def __init__(self, username: str, message: Optional[str] = None):
        default_message = f'Wrong password for user "{username}"'
        self.message = message or default_message
        log().info(self.message)
        super().__init__(self.message)


class UnknowUserException(Exception):
    def __init__(self, username: str, message: Optional[str] = None):
        default_message = f'Unknow user "{username}"'
        self.message = message or default_message
        log().info(self.message)
        super().__init__(self.message)


class InvalidCredentialException(Exception):
    def __init__(self, message: Optional[str] = None):
        default_message = "Invalid Credentials"
        self.message = message or default_message
        super().__init__(self.message)


class ImpossibleRollback(Exception):
    def __init__(self, message: Optional[str] = None):
        default_message = "Impossible to rollback the password"
        self.message = message or default_message
        super().__init__(self.message)
