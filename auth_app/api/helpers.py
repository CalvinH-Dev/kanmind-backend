from typing import Dict

from django.contrib.auth.models import User

from auth_app.api.serializers import EmailQuerySerializer
from auth_app.models import UserProfile


def getProfileForUser(user: User):
    try:
        return UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return None


def getValidEmail(params) -> str:
    serializer = EmailQuerySerializer(data=params)
    serializer.is_valid(raise_exception=True)

    return serializer.validated_data["email"]  # type: ignore
