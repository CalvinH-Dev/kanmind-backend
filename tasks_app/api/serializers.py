from rest_framework import serializers

from auth_app.api.helpers import CurrentUserProfileDefault
from auth_app.models import UserProfile
from boards_app.api.serializers import UserProfileSerializer
from tasks_app.api.helpers import verify_board_membership
from tasks_app.models import Comment, Task


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


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]


class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.fullname", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

    def create(self, validated_data):
        validated_data["author"] = UserProfile.objects.all().get(
            id=self.context["request"].user.id
        )
        return super().create(validated_data)
