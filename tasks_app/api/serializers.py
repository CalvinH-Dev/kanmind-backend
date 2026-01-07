from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from auth_app.api.helpers import CurrentUserProfileDefault
from boards_app.api.serializers import UserProfileSerializer
from boards_app.models import Board
from tasks_app.models import Task


class TaskBaseSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(write_only=True)
    reviewer_id = serializers.IntegerField(write_only=True)
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "assignee",
            "reviewer",
            "due_date",
        ]


class TaskUpdateSerializer(TaskBaseSerializer):
    pass


class TaskCreateSerializer(TaskBaseSerializer):
    creator = serializers.HiddenField(default=CurrentUserProfileDefault())
    comments_count = serializers.SerializerMethodField()

    class Meta(TaskBaseSerializer.Meta):
        fields = TaskBaseSerializer.Meta.fields + [
            "board",
            "creator",
            "comments_count",
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        creator_id = validated_data.get("creator").id

        board_id = validated_data.get("board").id
        board = Board.objects.all().get(id=board_id)

        not_board_owner_or_member = (
            creator_id != board.owner_id
            and not board.members.filter(id=creator_id).exists()
        )

        if not_board_owner_or_member:
            raise PermissionDenied("You cannot create a task for this board")

        return super().create(validated_data)
