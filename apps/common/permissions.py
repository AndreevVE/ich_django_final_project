from django.utils.translation import gettext_lazy as _
from rest_framework import permissions


class IsLandlord(permissions.BasePermission):
    message = _('Доступ разрешён только арендодателям.')


    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='Landlords').exists()
        )


class IsTenant(permissions.BasePermission):
    message = _('Доступ разрешён только арендаторам.')


    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='Tenants').exists()
        )


class IsOwner(permissions.BasePermission):
    message = _('Вы не являетесь владельцем этого объекта.')


    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.owner == request.user


class IsBookingOwnerOrLandlord(permissions.BasePermission):
    message = _('У вас нет прав на доступ к этой брони.')


    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.tenant == request.user or obj.listing.owner == request.userser