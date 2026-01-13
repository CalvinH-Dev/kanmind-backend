from django.contrib.auth.models import User

from auth_app.api.serializers import EmailQuerySerializer
from auth_app.models import UserProfile


def getProfileForUser(user: User):
    """
    Retrieve the UserProfile associated with the given User.

    Attempts to fetch the UserProfile object linked to the
    provided User. If no profile exists, the function returns
    None instead of raising a DoesNotExist exception.
    """
    try:
        return UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return None


def getValidEmail(params) -> str:
    """
    Extract and validate an email address from the given params.

    Uses EmailQuerySerializer to validate the incoming data.
    Raises a validation exception if the input is invalid.
    Returns the validated email string.
    """
    serializer = EmailQuerySerializer(data=params)
    serializer.is_valid(raise_exception=True)

    return serializer.validated_data["email"]  # type: ignore


class CurrentUserProfileDefault:
    """
    Default provider class for automatically using the current user's profile.

    This class is intended to be used as a default value provider
    in serializer fields where the current authenticated user's
    profile should be applied automatically.
    """

    requires_context = True

    def __call__(self, serializer_field):
        user = serializer_field.context["request"].user
        return UserProfile.objects.get(user=user)
