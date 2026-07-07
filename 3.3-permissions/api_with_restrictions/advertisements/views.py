from django.db import transaction
from django.db.models import Q

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from advertisements.models import Advertisement, Favorite, AdvertisementStatusChoices
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import (IsOwnerOrAdmin, IsOwnerOrReadOnly, CanFavorite)


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""
    
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action in ['favorite', 'unfavorite']:
            return [IsAuthenticated(), CanFavorite()]
        return [AllowAny()]

    def get_queryset(self):
        """Фильтрация черновиков."""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_authenticated:
            # Неавторизованные видят только OPEN и CLOSED
            return queryset.exclude(status=AdvertisementStatusChoices.DRAFT)
        
        if user.is_staff:
            # Админы видят все
            return queryset
        
        # Обычные пользователи видят:
        # - свои объявления (все статусы)
        # - чужие объявления (только OPEN и CLOSED)
        return queryset.filter(
            Q(creator=user) | 
            ~Q(status=AdvertisementStatusChoices.DRAFT)
        )

    def perform_create(self, serializer):
        """Создание объявления с проверкой лимита."""
        user = self.request.user
        
        with transaction.atomic():
            # Блокируем записи для избежания race condition
            open_count = Advertisement.objects.select_for_update().filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()
            
            if open_count >= 10:
                raise ValidationError(
                    "Нельзя создавать более 10 открытых объявлений."
                )
            
            serializer.save(creator=user)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """Добавление объявления в избранное."""
        advertisement = self.get_object()
        user = request.user
        
        # Проверяем, что пользователь не автор
        if advertisement.creator == user:
            return Response(
                {"detail": "Нельзя добавить свое объявление в избранное."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем, что объявление не в черновике
        if advertisement.status == AdvertisementStatusChoices.DRAFT:
            return Response(
                {"detail": "Нельзя добавить черновик в избранное."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создаем запись в избранном
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            advertisement=advertisement
        )
        
        if not created:
            return Response(
                {"detail": "Объявление уже в избранном."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unfavorite(self, request, pk=None):
        """Удаление объявления из избранного."""
        advertisement = self.get_object()
        user = request.user
        
        try:
            favorite = Favorite.objects.get(
                user=user,
                advertisement=advertisement
            )
            favorite.delete()
            return Response(
                {"detail": "Объявление удалено из избранного."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Favorite.DoesNotExist:
            return Response(
                {"detail": "Объявление не в избранном."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """Получение всех избранных объявлений пользователя."""
        user = request.user
        
        if not user.is_authenticated:
            return Response(
                {"detail": "Требуется авторизация."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        favorites = Favorite.objects.filter(user=user).select_related('advertisement')
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)