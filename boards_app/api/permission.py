from rest_framework.permissions import BasePermission

from boards_app.models import Board
from tasks_app.models import Task


class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if isinstance(obj, Task):
            obj = obj.board

        members = obj.members.all()
        owner_id = obj.owner_id
        is_member = members.filter(id=user.id).exists()
        is_owner = owner_id == user.id
        return is_member or is_owner


class IsBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if isinstance(obj, Task):
            obj = obj.board

        owner_id = obj.owner_id
        return owner_id == user.id
