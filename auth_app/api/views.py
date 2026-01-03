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

    def retrieve(self, request, *args, **kwargs):
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
