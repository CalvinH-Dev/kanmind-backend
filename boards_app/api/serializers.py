from django.contrib.auth.models import User
from rest_framework import serializers

from boards_app.models import Board


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    members = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=User.objects.all()
    )

    class Meta:
        model = Board
        fields = ["title", "members", "owner"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "member_count": instance.members.count(),
            "owner_id": instance.owner.id,
        }
