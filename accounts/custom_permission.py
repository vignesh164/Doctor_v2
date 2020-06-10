from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return 'Doctor' in list(request.user.groups.values_list('name', flat=True))


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return 'Patient' in list(request.user.groups.values_list('name', flat=True))


class IsMedical(BasePermission):
    def has_permission(self, request, view):
        return 'Medical' in list(request.user.groups.values_list('name', flat=True))
