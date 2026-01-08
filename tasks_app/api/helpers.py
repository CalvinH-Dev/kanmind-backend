from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from boards_app.models import Board


def has_board_access(board: Board, profile_id: int) -> bool:
    is_member: bool = board.members.filter(id=profile_id).exists()
    is_owner: bool = board.owner_id == profile_id or False
    return is_member or is_owner


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
