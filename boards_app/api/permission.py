from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from tasks_app.models import Comment, Task


class IsBoardMemberOrOwner(BasePermission):
    """
    Custom permission to allow access only if the user is a board member or the
    board owner.

    This permission class checks both view-level and object-level access. At
    the view level it obtains the task by its ID and verifies if the request
    user belongs to the board's members or is the board owner. At the object
    level, it handles Task and Comment objects and resolves the board to
    perform the same membership and ownership checks.
    """

    def has_permission(self, request, view):
        task_id = view.kwargs.get("task_id")
        if not task_id:
            return True

        task = get_object_or_404(Task.objects.all(), pk=task_id)

        board = task.board
        user = request.user

        is_member = board.members.filter(id=user.id).exists()
        is_owner = board.owner_id == user.id

        return is_member or is_owner

    def has_object_permission(self, request, view, obj):
        user = request.user

        if isinstance(obj, Task):
            obj = obj.board

        if isinstance(obj, Comment):
            obj = obj.task.board

        members = obj.members.all()
        owner_id = obj.owner_id
        is_member = members.filter(id=user.id).exists()
        is_owner = owner_id == user.id
        return is_member or is_owner


class IsBoardOwner(BasePermission):
    """
    Custom permission to allow access only if the user is the board owner.

    This permission is determined at object level. For Task objects, it
    resolves the board before checking ownership.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if isinstance(obj, Task):
            obj = obj.board

        owner_id = obj.owner_id
        return owner_id == user.id
