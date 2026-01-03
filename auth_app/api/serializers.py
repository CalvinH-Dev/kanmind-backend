from django.contrib.auth.models import User
from rest_framework import serializers

from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=150, write_only=True)
    repeated_password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ["email", "fullname", "password", "repeated_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"error": "Password and repeated password don't match"}
            )
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        pw = validated_data.pop("password")
        validated_data.pop("repeated_password")
        fullname = validated_data.pop("fullname")
        email = validated_data["email"]

        account = User(email=email, username=email)
        account.set_password(pw)
        account.save()

        first_name, *last_parts = fullname.strip().split()
        last_name = " ".join(last_parts) if last_parts else ""
        profile = UserProfile(user=account, fullname=fullname)
        profile.save()

        account.first_name = first_name
        account.last_name = last_name
        account.save()

        return account
