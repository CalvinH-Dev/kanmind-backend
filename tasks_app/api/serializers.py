from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from auth_app.api.helpers import CurrentUserProfileDefault
from boards_app.api.serializers import UserProfileSerializer
from tasks_app.api.helpers import has_board_access
from tasks_app.models import Task


def verify_board_membership(board, creator_id, validated_data):
    assignee_id = validated_data.get("assignee_id", None)
    reviewer_id = validated_data.get("reviewer_id", None)

    if not has_board_access(board, creator_id):
        raise PermissionDenied("You cannot create a task for this board.")

    if assignee_id:
        if not has_board_access(board, assignee_id):
            raise serializers.ValidationError(
                "Assignee must be a member of the board."
            )
    if reviewer_id:
        if not has_board_access(board, reviewer_id):
            raise serializers.ValidationError(
                "Reviewer must be a member of the board."
            )


class TaskBaseSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )
    reviewer_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )
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

    def update(self, instance, validated_data):
        board = instance.board
        creator_id = instance.creator_id
        verify_board_membership(board, creator_id, validated_data)
        return super().update(instance, validated_data)


class TaskListSerializer(TaskBaseSerializer):
    comments_count = serializers.SerializerMethodField()

    class Meta(TaskBaseSerializer.Meta):
        fields = TaskBaseSerializer.Meta.fields + ["comments_count", "board"]

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskCreateSerializer(TaskListSerializer):
    creator = serializers.HiddenField(default=CurrentUserProfileDefault())

    class Meta(TaskListSerializer.Meta):
        fields = TaskListSerializer.Meta.fields + [
            "creator",
        ]

    def create(self, validated_data):
        board = validated_data.get("board")
        creator_id = validated_data.get("creator").id
        verify_board_membership(board, creator_id, validated_data)

        return super().create(validated_data)
