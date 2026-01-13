from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.api.helpers import getProfileForUser, getValidEmail
from auth_app.api.serializers import LoginSerializer, RegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    """
    API view for registering a new user.

    Uses the RegistrationSerializer to handle incoming POST requests
    with registration details and create a new user and profile.
    """

    permission_classes = []
    serializer_class = RegistrationSerializer


class LoginView(ObtainAuthToken):
    """
    API view to authenticate a user and return a token.

    Accepts login credentials via POST, validates them using the
    LoginSerializer, and returns an auth token along with user info.
    """

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.

        Validates the request data, retrieves the authenticated user
        and their full name, and returns a Response containing the
        token and basic user information.
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]  # type: ignore
        fullname = serializer.validated_data["fullname"]  # type: ignore
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "fullname": fullname,
                "email": user.email,
                "user_id": user.pk,
            }
        )


class EmailCheckView(generics.RetrieveAPIView):
    """
    API view to check if a user exists by email.

    Requires the request to be authenticated. Looks up a User by
    validated email query parameter and returns their id, email,
    and full name if found.
    """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a user by email.

        Extracts and validates the email from query parameters,
        looks up a matching user, and returns a Response with user
        profile details. If not found, returns 404 status.
        """
        email = getValidEmail(request.query_params)

        if not (user := self.queryset.filter(email=email).first()):
            return Response(status=404)

        if not (profile := getProfileForUser(user)):
            return Response(status=404)

        return Response(
            {
                "id": user.pk,
                "email": user.email,
                "fullname": profile.fullname,
            }
        )
