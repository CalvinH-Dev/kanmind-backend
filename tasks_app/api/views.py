from django.db.models import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from auth_app.models import UserProfile
from boards_app.api.permission import IsBoardMemberOrOwner
from boards_app.models import Board
from tasks_app.api.permissions import IsTaskCreatorOrBoardOwner
from tasks_app.api.serializers import (
    TaskBaseSerializer,
    TaskCreateSerializer,
    TaskListSerializer,
    TaskUpdateSerializer,
)
from tasks_app.models import Task


class AssignedToMeView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskListSerializer

    def get_queryset(self) -> QuerySet[Task]:
        user = self.request.user
        profile = UserProfile.objects.all().filter(user=user).first()
        return profile.tasks_assigned.all()


class ReviewingView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskListSerializer

    def get_queryset(self) -> QuerySet[Task]:
        user = self.request.user
        profile = UserProfile.objects.all().filter(user=user).first()
        return profile.tasks_reviewing.all()


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
