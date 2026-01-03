from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.api.helpers import getProfileForUser, getValidEmail
from auth_app.api.serializers import LoginSerializer, RegistrationSerializer
from auth_app.models import UserProfile


class RegistrationView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = RegistrationSerializer


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
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
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    # serializer_class = RegistrationSerializer

    def retrieve(self, request, *args, **kwargs):
        users = self.queryset
        email = getValidEmail(request.query_params)
        user = users.filter(email=email).first()

        if not user:
            return Response(status=404)

        profile = getProfileForUser(user)

        if profile:
            return Response(
                {
                    "id": user.pk,
                    "email": user.email,
                    "fullname": profile.fullname,
                }
            )

        return Response(status=404)
