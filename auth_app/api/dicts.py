from typing import Type, TypedDict


class RegistrationUserDict(TypedDict):
    email: str
    password: str
    repeated_password: str
    fullname: str


class LoginUserDict(TypedDict):
    email: str
    password: str
