from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsBoardMemberOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = obj.user

        if request.method in SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return request.user and request.user.is_superuser
        else:
            return request.user and request.user == user
