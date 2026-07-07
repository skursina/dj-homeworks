from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор для объявления."""
    creator = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    favorites_count = serializers.IntegerField(source='favorited_by.count', read_only=True)

    class Meta:
        model = Advertisement
        fields = (
            'id', 'title', 'description', 'creator', 
            'status', 'created_at', 'updated_at',
            'is_favorited', 'favorites_count'
        )
        read_only_fields = ('creator', 'created_at', 'updated_at')

    def get_is_favorited(self, obj):
        """Проверяет, добавил ли текущий пользователь объявление в избранное."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(
                user=request.user,
                advertisement=obj
            ).exists()
        return False

    def validate_status(self, value):
        """Валидация статуса при создании."""
        if self.instance is None:  # Только при создании
            user = self.context['request'].user
            if value == AdvertisementStatusChoices.OPEN:
                open_count = Advertisement.objects.filter(
                    creator=user,
                    status=AdvertisementStatusChoices.OPEN
                ).count()
                if open_count >= 10:
                    raise ValidationError(
                        "Нельзя создавать более 10 открытых объявлений."
                    )
        return value

    def validate(self, data):
        """Валидация при обновлении."""
        if self.instance and 'status' in data:
            user = self.context['request'].user
            new_status = data['status']
            
            # Проверяем лимит открытых только при переходе в OPEN
            if new_status == AdvertisementStatusChoices.OPEN:
                open_count = Advertisement.objects.filter(
                    creator=user,
                    status=AdvertisementStatusChoices.OPEN
                ).count()
                
                # Если текущее объявление было CLOSED или DRAFT
                if self.instance.status != AdvertisementStatusChoices.OPEN:
                    if open_count >= 10:
                        raise ValidationError(
                            "Нельзя иметь более 10 открытых объявлений."
                        )
        return data

    def create(self, validated_data):
        """Создание объявления с простановкой creator."""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных объявлений."""
    advertisement = AdvertisementSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'advertisement', 'created_at')
        read_only_fields = ('user', 'created_at')