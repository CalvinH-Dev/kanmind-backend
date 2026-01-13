from rest_framework import serializers

from auth_app.api.helpers import CurrentUserProfileDefault
from auth_app.models import UserProfile
from boards_app.models import Board


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.

    Includes the profile ID, full name, and uses a custom method
    field to fetch the linked user's email.
    """

    email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["id", "email", "fullname"]

    def get_email(self, obj):
        return obj.user.email


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Board details.

    Includes nested UserProfileSerializer representations for
    members and the owner's ID. Useful for detail views.
    """

    members = UserProfileSerializer(many=True, read_only=True)
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "members",
            "owner_id",
        ]


class UpdateBoardSerializer(serializers.ModelSerializer):
    """
    Serializer used for updating Board instances.

    Shows read-only nested data for the owner and members, while
    allowing the members field to be updated via its IDs.
    """

    owner_data = UserProfileSerializer(source="owner", read_only=True)
    members_data = UserProfileSerializer(
        source="members", many=True, read_only=True
    )

    class Meta:
        model = Board
        fields = ["id", "title", "members", "owner_data", "members_data"]
        extra_kwargs = {"members": {"write_only": True}}


class BoardListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing boards.

    Automatically sets the current authenticated user's profile
    as the owner using a hidden default. Also provides a count of
    members via a custom method field.
    """

    owner = serializers.HiddenField(default=CurrentUserProfileDefault())
    member_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "members",
            "owner",
            "member_count",
            "owner_id",
        ]
        extra_kwargs = {"members": {"write_only": True}}

    def get_member_count(self, obj):
        return obj.members.count()
