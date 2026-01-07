from rest_framework.permissions import BasePermission


class IsTaskCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        creator_id = obj.creator_id
        return creator_id == user.id
