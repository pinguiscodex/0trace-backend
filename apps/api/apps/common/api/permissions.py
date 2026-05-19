from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    owner_field = "owner"

    def has_object_permission(self, request, view, obj) -> bool:
        return getattr(obj, self.owner_field, None) == request.user


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in {"GET", "HEAD", "OPTIONS"}:
            return True
        return bool(request.user and request.user.is_staff)

