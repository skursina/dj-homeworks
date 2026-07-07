from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """Разрешение на редактирование только для создателя объявления или админа."""
    
    def has_object_permission(self, request, view, obj):
        # Администраторы имеют право на любые действия
        if request.user.is_staff:
            return True
        
        # Разрешение на редактирование только для создателя объявления
        return obj.creator == request.user


class IsOwnerOrReadOnly(BasePermission):
    """Разрешение на просмотр только для владельца (для черновиков)."""
    
    def has_object_permission(self, request, view, obj):
        # Безопасные методы (GET, HEAD, OPTIONS) разрешены всем
        if request.method in SAFE_METHODS:
            return True
        
        # Для остальных методов - только владелец или админ
        return obj.creator == request.user or request.user.is_staff


class CanFavorite(BasePermission):
    """Разрешение на добавление в избранное."""
    
    def has_object_permission(self, request, view, obj):
        # Нельзя добавить свое объявление в избранное
        return obj.creator != request.user