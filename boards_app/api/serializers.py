from django.contrib.auth.models import User
from rest_framework import serializers

from auth_app.api.helpers import CurrentUserProfileDefault
from auth_app.models import UserProfile
from boards_app.models import Board


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["id", "email", "fullname"]

    def get_email(self, obj):
        return obj.user.email


class BoardDetailSerializer(serializers.ModelSerializer):
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
    owner_data = UserProfileSerializer(source="owner", read_only=True)
    members_data = UserProfileSerializer(
        source="members", many=True, read_only=True
    )

    class Meta:
        model = Board
        fields = ["id", "title", "members", "owner_data", "members_data"]
        extra_kwargs = {"members": {"write_only": True}}


class BoardListSerializer(serializers.ModelSerializer):
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
