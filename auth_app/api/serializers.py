from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from auth_app.models import UserProfile


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        attrs["user"] = user

        profile = getattr(user, "userprofile", None)
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
        pw = validated_data.pop("password")
        validated_data.pop("repeated_password")
        fullname = validated_data.pop("fullname")
        email = validated_data.pop("email")

        user = User(email=email, username=email)
        user.set_password(pw)
        user.save()

        UserProfile.objects.create(user=user, fullname=fullname)

        first_name, *last_parts = fullname.strip().split()
        last_name = " ".join(last_parts) if last_parts else ""
        user.first_name = first_name
        user.last_name = last_name
        user.save()

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
