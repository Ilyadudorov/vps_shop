from pyexpat.errors import messages
from rest_framework import permissions


class IsOwnerCreateReadUpdateDelete(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user