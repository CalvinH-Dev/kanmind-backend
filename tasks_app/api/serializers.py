from rest_framework import serializers

from auth_app.api.helpers import CurrentUserProfileDefault
from boards_app.api.serializers import UserProfileSerializer
from tasks_app.api.helpers import check_members_of_board
from tasks_app.models import Task


def check_users_with_board(board, creator_id, validated_data):
    assignee_id = validated_data.get("assignee_id", None)
    reviewer_id = validated_data.get("reviewer_id", None)

    check_members_of_board(board, creator_id, assignee_id, reviewer_id)


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
        check_users_with_board(board, creator_id, validated_data)
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
        check_users_with_board(board, creator_id, validated_data)

        return super().create(validated_data)
