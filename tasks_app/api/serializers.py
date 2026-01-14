from rest_framework import serializers

from auth_app.api.helpers import CurrentUserProfileDefault
from auth_app.models import UserProfile
from boards_app.api.serializers import UserProfileSerializer
from tasks_app.api.helpers import verify_board_membership
from tasks_app.models import Comment, Task


class TaskBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for Task model shared by list, create, and update.

    Provides read/write fields for assignee and reviewer via IDs,
    and nested UserProfileSerializer for their read-only representation.
    """

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
    """
    Serializer for updating a Task instance.

    Calls `verify_board_membership` to ensure the updater is
    allowed to modify board-related fields before delegating
    to the base update logic.
    """

    def update(self, instance, validated_data):
        board = instance.board
        creator_id = instance.creator_id
        verify_board_membership(board, creator_id, validated_data)
        return super().update(instance, validated_data)


class TaskListSerializer(TaskBaseSerializer):
    """
    Serializer used for listing tasks.

    Includes a custom SerializerMethodField to count related comments
    and also contains the board relationship.
    """

    comments_count = serializers.SerializerMethodField()

    class Meta(TaskBaseSerializer.Meta):
        fields = TaskBaseSerializer.Meta.fields + ["comments_count", "board"]

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskCreateSerializer(TaskListSerializer):
    """
    Serializer for creating a Task.

    Adds a hidden default for `creator`, which uses
    CurrentUserProfileDefault to auto-assign the profile of the
    authenticated user. It also ensures board membership via
    `verify_board_membership` before creation.
    """

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


class BoardTaskListSerializer(TaskBaseSerializer):
    """
    Serializer used for listing tasks.

    Includes a custom SerializerMethodField to count related comments
    and also contains the board relationship.
    """

    comments_count = serializers.SerializerMethodField()

    class Meta(TaskBaseSerializer.Meta):
        fields = TaskBaseSerializer.Meta.fields + ["comments_count"]

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for comment details.

    Represents the author by their full name and includes
    timestamp and content information.
    """

    author = serializers.CharField(source="author.fullname", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]


class CommentListAndCreateSerializer(CommentDetailSerializer):
    """
    Serializer for listing and creating comments.

    Inherits the detail fields, and sets the author based on
    the authenticated user's profile during creation.
    """

    class Meta(CommentDetailSerializer.Meta):
        fields = CommentDetailSerializer.Meta.fields + []
        extra_kwargs = {
            "content": {
                "required": True,
                "allow_blank": False,
            },
        }

    def create(self, validated_data):
        validated_data["author"] = UserProfile.objects.all().get(
            id=self.context["request"].user.id
        )
        return super().create(validated_data)
