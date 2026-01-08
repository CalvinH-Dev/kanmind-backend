from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from auth_app.models import UserProfile
from boards_app.api.permission import IsBoardMemberOrOwner
from tasks_app.api.helpers import has_board_access
from tasks_app.api.permissions import (
    IsCommentCreator,
    IsTaskCreatorOrBoardOwner,
)
from tasks_app.api.serializers import (
    CommentListAndCreateSerializer,
    TaskBaseSerializer,
    TaskCreateSerializer,
    TaskListSerializer,
    TaskUpdateSerializer,
)
from tasks_app.models import Comment, Task


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

    def list(self, request, *args, **kwargs):
        raise NotFound()

    def retrieve(self, request, *args, **kwargs):
        raise NotFound()

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


class CommentsListCreateAPI(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]
    serializer_class = CommentListAndCreateSerializer

    def get_queryset(self):
        task_id = self.kwargs["task_id"]
        get_object_or_404(Task.objects.all(), pk=task_id)
        comments = Comment.objects.all().filter(task_id=task_id)
        return comments

    def perform_create(self, serializer):
        task_id = self.kwargs["task_id"]
        serializer.save(task_id=task_id)


class CommentDeleteAPI(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCommentCreator]

    def get_object(self):
        task_id = self.kwargs["task_id"]
        pk = self.kwargs["pk"]

        task = get_object_or_404(Task.objects.all(), pk=task_id)
        comment = get_object_or_404(task.comments, pk=pk)
        self.check_object_permissions(self.request, comment)

        return comment
