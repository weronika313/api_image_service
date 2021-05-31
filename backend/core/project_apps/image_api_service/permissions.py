from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.plan.can_generate_expiring_links


class HasAbilityToGenerateExpiringLinks(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.plan.can_generate_expiring_links
