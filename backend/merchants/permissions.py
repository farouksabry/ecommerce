from rest_framework.permissions import BasePermission

class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and (
                request.user.is_staff
                or hasattr(request.user, "merchant")
            )
        )
