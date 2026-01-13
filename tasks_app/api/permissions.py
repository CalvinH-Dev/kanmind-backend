from rest_framework.permissions import BasePermission


class IsTaskCreator(BasePermission):
    """
    Permission class that allows access only to the creator of a task.

    This object-level permission checks that the authenticated user making
    the request is the same user that originally created the task instance.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        creator_id = obj.creator_id
        return creator_id == user.id


class IsTaskCreatorOrBoardOwner(BasePermission):
    """
    Permission class to allow access to either the task creator or board owner.

    This object-level permission checks two conditions:
    1. The authenticated user is the creator of the task.
    2. The authenticated user is the owner of the board that the task belongs
    to.
    Access will be granted if either condition is True.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        is_creator = hasattr(obj, "creator") and obj.creator_id == user.id

        is_board_owner = (
            hasattr(obj, "board") and obj.board.owner_id == user.id
        )

        return is_creator or is_board_owner


class IsCommentCreator(BasePermission):
    """
    Permission class that allows access only to the author of a comment.

    This object-level permission ensures that only the comment's author
    (matching `author_id`) may modify or delete the comment.
    """

    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        return obj.author_id == user_id
