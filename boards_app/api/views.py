from django.db.models import Q, QuerySet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from auth_app.models import UserProfile
from boards_app.api.serializers import (
    BoardDetailSerializer,
    BoardListSerializer,
)
from boards_app.models import Board


class BoardsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "create":
            return BoardListSerializer
        return BoardDetailSerializer

    def get_queryset(self) -> QuerySet[Board]:
        user = self.request.user
        profile = UserProfile.objects.all().filter(user=user).first()
        return Board.objects.filter(
            Q(owner=profile) | Q(members=profile)
        ).distinct()
