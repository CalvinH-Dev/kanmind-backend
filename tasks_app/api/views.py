from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from boards_app.api.permission import IsBoardMemberOrOwner
from tasks_app.api.permissions import IsTaskCreatorOrBoardOwner
from tasks_app.api.serializers import (
    TaskBaseSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
)
from tasks_app.models import Task


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()

    def get_permissions(self):
        if self.action == "partial_update":
            return [IsAuthenticated(), IsBoardMemberOrOwner()]
        elif self.action == "destroy":
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwner()]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "create":
            return TaskCreateSerializer
        if self.action == "partial_update":
            return TaskUpdateSerializer
        return TaskBaseSerializer
