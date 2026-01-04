from typing import Any, Dict, Iterable, MutableMapping

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from auth_app.api.dicts import LoginUserDict, RegistrationUserDict
from auth_app.models import UserProfile
from core.helpers import split_fullname


def clean_up_data(data, keys: Iterable[str]) -> None:
    for key in keys:
        data.pop(key, None)


def save_user(data: RegistrationUserDict):
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
    email = attrs.get("email")
    password = attrs.get("password")

    user = authenticate(username=email, password=password)
    if not user:
        raise serializers.ValidationError("Invalid email or password")
    return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate_user(attrs)
        attrs["user"] = user

        profile = user.userprofile  # type: ignore
        attrs["fullname"] = profile.fullname if profile else ""
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=150, write_only=True)
    repeated_password = serializers.CharField(max_length=100, write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email already exists",
            )
        ],
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "repeated_password",
            "fullname",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"error": "Password and repeated password don't match"}
            )
        return attrs

    def create(self, validated_data):
        user = save_user(validated_data)

        fullname = validated_data.pop("fullname")
        UserProfile.objects.create(user=user, fullname=fullname)

        return user

    def to_representation(self, instance):
        profile = getattr(instance, "userprofile", None)
        fullname = profile.fullname if profile else ""
        token = Token.objects.create(user=instance)
        return {
            "token": token.key,
            "fullname": fullname,
            "email": instance.email,
            "user_id": instance.id,
        }


class EmailQuerySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
