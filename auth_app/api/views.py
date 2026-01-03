from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from auth_app.api.serializers import LoginSerializer, RegistrationSerializer


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
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "fullname": fullname,
                "email": user.email,
                "user_id": user.pk,
            }
        )
