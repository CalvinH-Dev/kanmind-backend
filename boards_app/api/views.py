from django.db.models import Q, QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from auth_app.models import UserProfile
from boards_app.api.permission import IsBoardMemberOrOwner, IsBoardOwner
from boards_app.api.serializers import (
    BoardDetailSerializer,
    BoardListSerializer,
    UpdateBoardSerializer,
)
from boards_app.models import Board


class BoardsViewSet(ModelViewSet):
    """
    ViewSet for Board objects that handles permissions, queryset filtering,
    and serializer selection based on the action being performed.

    Uses custom permissions to ensure that only board members or the board
    owner have access, and only the board owner can delete.
    """

    permission_classes = [IsAuthenticated & IsBoardMemberOrOwner]
    queryset = Board.objects.all()

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAuthenticated(), IsBoardOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return BoardListSerializer
        if self.action == "partial_update":
            return UpdateBoardSerializer
        return BoardDetailSerializer

    def get_queryset(self) -> QuerySet[Board]:
        if self.action == "list":
            user = self.request.user
            profile = UserProfile.objects.filter(user=user).first()
            # Only return boards where the profile is owner or member
            return Board.objects.filter(
                Q(owner=profile) | Q(members=profile)
            ).distinct()

        return Board.objects.all()
