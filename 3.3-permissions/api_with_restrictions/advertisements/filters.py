from django_filters import rest_framework as filters
from django.db.models import Q

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    
    created_at = filters.DateFromToRangeFilter()
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    
    class Meta:
        model = Advertisement
        fields = {
            'status': ['exact'],
            'creator': ['exact'],
            'title': ['icontains'],  
        }
    
    def filter_is_favorited(self, queryset, name, value):
        """Фильтр для избранных объявлений."""
        user = self.request.user
        
        if not user.is_authenticated:
            return queryset.none()
        
        if value:  # Только избранные
            return queryset.filter(favorited_by__user=user)
        else:  # Все, кроме избранных
            return queryset.exclude(favorited_by__user=user)