from rest_framework.permissions import BasePermission


class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        members = obj.members.all()
        owner_id = obj.owner_id
        is_member = members.filter(id=user.id).exists()
        is_owner = owner_id == user.id
        return is_member or is_owner


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        owner_id = obj.owner_id
        return owner_id == user.id
