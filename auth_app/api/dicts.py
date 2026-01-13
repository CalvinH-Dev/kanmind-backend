from typing import TypedDict


class RegistrationUserDict(TypedDict):
    """
    Dictionary type for user registration data.

    This typed dictionary defines the expected structure for
    registration input, including:
    - email: the user's email address
    - password: the user's password
    - repeated_password: the confirmation of the password
    - fullname: the user's full name
    """

    email: str
    password: str
    repeated_password: str
    fullname: str


class LoginUserDict(TypedDict):
    """
    Dictionary type for user login data.

    This typed dictionary defines the expected structure for
    login input, including:
    - email: the user's email address
    - password: the user's password
    """

    email: str
    password: str
