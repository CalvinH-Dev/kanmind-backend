from rest_framework import generics
from rest_framework.response import Response

from auth_app.api.serializers import RegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = RegistrationSerializer

    # def create(request, *args, **kwargs) -> Response:
    #     return Response()
