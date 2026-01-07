import re

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from boards_app.models import Board


def is_board_member_or_owner(board: Board, profile_id: int) -> bool:
    is_member: bool = board.members.filter(id=profile_id).exists()
    is_owner: bool = board.owner_id == profile_id or False
    return is_member or is_owner


def check_members_of_board(
    board: Board,
    creator_id: int | None,
    assignee_id: int | None,
    reviewer_id: int | None,
):
    if not is_board_member_or_owner(board, creator_id):
        raise PermissionDenied("You cannot create a task for this board")

    if assignee_id:
        if not is_board_member_or_owner(board, assignee_id):
            raise serializers.ValidationError(
                "Assignee must be a member of the board."
            )
    if reviewer_id:
        if not is_board_member_or_owner(board, reviewer_id):
            raise serializers.ValidationError(
                "Reviewer must be a member of the board."
            )
