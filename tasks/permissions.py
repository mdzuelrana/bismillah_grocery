from rest_framework import permissions



class IsSellerOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role in ['admin', 'seller']

    def has_object_permission(self, request, view, obj):

        if request.user.role == 'admin':
            return True

        if request.user.role == 'seller':
            return obj.seller == request.user

        return False

class IsReviewOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
