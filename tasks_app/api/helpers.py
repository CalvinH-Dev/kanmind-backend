from boards_app.models import Board


def has_board_access(board: Board, profile_id: int) -> bool:
    is_member: bool = board.members.filter(id=profile_id).exists()
    is_owner: bool = board.owner_id == profile_id or False
    return is_member or is_owner
