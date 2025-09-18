from rest_framework.permissions import BasePermission

# Define role groups here
ROLE_GROUPS = {
    "ADMIN": "Admin",
    "FINANCE": "Finance",
    "SUPPORT": "Support",
    "DEVELOPER": "Developer",
    "CUSTOMER": "Customer",
}

class IsInGroup(BasePermission):
    """
    Custom permission to check if the user belongs to any of the given groups.
    Usage: IsInGroup(groups=["Admin", "Finance"])
    """

    def __init__(self, groups=None):
        self.groups = groups or []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        user_groups = request.user.groups.values_list("name", flat=True)
        return any(group in user_groups for group in self.groups)


class ReadOnly(BasePermission):
    """Allow read-only access for unauthenticated users."""

    def has_permission(self, request, view):
        return request.method in ("GET", "HEAD", "OPTIONS")
