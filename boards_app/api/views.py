from django.db.models import Q
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
        boards = (
            self.get_queryset()
            .filter(Q(owner=request.user) | Q(members=request.user))
            .distinct()
        )

        serializer = self.get_serializer(boards, many=True)
        return Response(serializer.data)
