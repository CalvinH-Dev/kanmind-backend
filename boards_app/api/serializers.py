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
            "owner",
            "owner_id",
        ]


class BoardListSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=CurrentUserProfileDefault())
    members = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=UserProfile.objects.all()
    )
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

    def get_member_count(self, obj):
        return obj.members.count()
