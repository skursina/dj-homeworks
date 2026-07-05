from django_filters import rest_framework as filters
from .models import Stock

class StockFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search', label='Поиск по адресу или продуктам')

    class Meta:
        model = Stock
        fields = ['products']   

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            address__icontains=value
        ) | queryset.filter(
            products__title__icontains=value
        ) | queryset.filter(
            products__description__icontains=value
        ).distinct()  