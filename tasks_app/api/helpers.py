from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from boards_app.models import Board


def has_board_access(board: Board, profile_id: int) -> bool:
    """
    Return True if the given profile has access to the board.

    Checks if the profile ID is either a member of the board or
    the board's owner. Returns a boolean accordingly.
    """
    is_member: bool = board.members.filter(id=profile_id).exists()
    is_owner: bool = board.owner_id == profile_id or False
    return is_member or is_owner


def verify_board_membership(board, creator_id, validated_data):
    """
    Ensure that users referenced in validated data belong to the board.

    Raises a PermissionDenied error if the creator does not have
    access to the board. Raises a ValidationError if the assignee
    or reviewer IDs in validated_data are not board members.
    """
    assignee_id = validated_data.get("assignee_id", None)
    reviewer_id = validated_data.get("reviewer_id", None)

    # Check if the creator has access to the board
    if not has_board_access(board, creator_id):
        raise PermissionDenied("You cannot create a task for this board.")

    # Validate that the assignee is a board member if provided
    if assignee_id:
        if not has_board_access(board, assignee_id):
            raise serializers.ValidationError(
                "Assignee must be a member of the board."
            )

    # Validate that the reviewer is a board member if provided
    if reviewer_id:
        if not has_board_access(board, reviewer_id):
            raise serializers.ValidationError(
                "Reviewer must be a member of the board."
            )
