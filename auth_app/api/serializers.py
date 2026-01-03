from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=150, write_only=True)
    repeated_password = serializers.CharField(max_length=100, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "repeated_password",
            "fullname",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

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
        email = validated_data["email"]

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
