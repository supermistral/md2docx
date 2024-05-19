from ..exceptions import BaseException


class UserAlreadyExists(BaseException):
    STATUS = 400
    CODE = "UserAlreadyExists"
    MESSAGE = "User with email '{email}' already exists."
