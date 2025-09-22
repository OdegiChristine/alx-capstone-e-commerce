from rest_framework import permissions

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Only sellers can create, update, or delete products.
    Customers and unauthenticated users can only read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and getattr(request.user, "is_seller", False)
            and obj.seller == request.user
        )

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS - always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and getattr(request.user, "is_seller", False)
        )
