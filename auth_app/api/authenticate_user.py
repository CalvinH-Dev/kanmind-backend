from typing import Iterable

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from auth_app.api.dicts import LoginUserDict, RegistrationUserDict
from core.helpers import split_fullname


def clean_up_data(data, keys: Iterable[str]) -> None:
    """
    Remove specified keys from a dictionary in place.

    Iterates over the provided list of keys and removes each one
    from the data dictionary if it exists. This helps prepare
    the dictionary for further processing where certain keys
    are no longer needed.
    """
    for key in keys:
        data.pop(key, None)


def save_user(data: RegistrationUserDict):
    """
    Create and save a new User instance from registration data.

    Extracts the password, email, and full name from the
    registration dictionary. Removes redundant items from the
    dictionary, constructs the User object, and sets its password.
    Also splits the full name into first and last name fields
    before saving and returns the created User.
    """
    pw = data["password"]
    email = data["email"]
    fullname = data["fullname"]

    clean_up_data(
        data,
        ["password", "repeated_password", "email"],
    )

    user = User(email=email, username=email)
    user.set_password(pw)
    user.first_name, user.last_name = split_fullname(fullname)
    user.save()

    return user


def authenticate_user(attrs: LoginUserDict):
    """
    Authenticate a user based on provided login credentials.

    Given a dictionary with email and password, attempts to
    authenticate the user using Django's authentication system.
    Raises a validation error when credentials are invalid,
    otherwise returns the authenticated User instance.
    """
    email = attrs.get("email")
    password = attrs.get("password")

    user = authenticate(username=email, password=password)
    if not user:
        raise serializers.ValidationError("Invalid email or password")
    return user
