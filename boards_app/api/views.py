from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from boards_app.api.serializers import BoardSerializer
from boards_app.models import Board


class BoardsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        return super().list(request, *args, **kwargs)
