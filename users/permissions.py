from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Класс ограничений по доступу для владельцев курсов и уроков."""

    def has_object_permission(self, request, view, obj):
        """Метод для проверки прав доступа у пользователя на объект."""

        if obj.owner == request.user:
            return True
        return False


class IsUserOwner(BasePermission):
    """Класс ограничений по доступу для владельцев профилей пользователя."""

    def has_object_permission(self, request, view, obj):
        """Метод для проверки прав доступа у пользователя на объект."""

        if request.user == obj:
            return True
        return False
