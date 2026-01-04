from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        members = obj.members.all()
        owner_id = obj.owner_id
        if request.method in SAFE_METHODS:
            is_member = members.filter(id=user.id).exists()
            is_owner = owner_id == user.id
            return is_member or is_owner
        elif request.method == "DELETE":
            return request.user and request.user.is_superuser
        else:
            return request.user and request.user == user
