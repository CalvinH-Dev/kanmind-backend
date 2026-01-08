from rest_framework.permissions import BasePermission


class IsTaskCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        creator_id = obj.creator_id
        return creator_id == user.id


class IsTaskCreatorOrBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        is_creator = hasattr(obj, "creator") and obj.creator_id == user.id

        is_board_owner = (
            hasattr(obj, "board") and obj.board.owner_id == user.id
        )

        return is_creator or is_board_owner


class IsCommentCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        return obj.author_id == user_id
