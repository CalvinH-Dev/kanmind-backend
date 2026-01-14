from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from auth_app.api.authenticate_user import authenticate_user, save_user
from auth_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.

    Includes the profile ID, full name, and uses a custom method
    field to fetch the linked user's email.
    """

    email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["id", "email", "fullname"]

    def get_email(self, obj):
        return obj.user.email


class LoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login input and validation.

    Defines the expected fields for login, including email and
    password. After validation, attaches the authenticated user
    and their full name to the validated data.
    """

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
    """
    Serializer for registering a new user.

    Handles incoming registration data, enforces email
    uniqueness, matches password fields, and creates the User
    along with a related UserProfile. Returns a token and
    profile information on output.
    """

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
        """
        Customize serialization output after user creation.

        Includes an authentication token, the user's full name,
        email, and user ID in the returned data.
        """
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
    """
    Serializer for validating email query parameters.

    Ensures that the email field is present and conforms to a
    valid email format.
    """

    email = serializers.EmailField(required=True)
