from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Measurement, Sensor
from .serializers import (SensorSerializer,
                          SensorDetailSerializer,
                          MeasurementCreateSerializer)


@extend_schema_view(
    list=extend_schema(summary="Список датчиков", description="Возвращает список всех датчиков с ID, названием и описанием."),
    create=extend_schema(summary="Создать датчик", description="Создаёт новый датчик с указанными name и description."),
    retrieve=extend_schema(summary="Детальная информация о датчике", description="Возвращает полную информацию о датчике, включая список его измерений."),
    update=extend_schema(summary="Полное обновление датчика"),
    partial_update=extend_schema(summary="Частичное обновление датчика"),
)
class SensorViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с датчиками:
    - GET /sensors/ – список датчиков (SensorSerializer)
    - POST /sensors/ – создание датчика (SensorSerializer)
    - GET /sensors/{id}/ – детальная информация (SensorDetailSerializer)
    - PATCH /sensors/{id}/ – частичное обновление (SensorSerializer)
    - PUT /sensors/{id}/ – полное обновление (не используем, но оставим)
    - DELETE /sensors/{id}/ – удаление (не используется, но можно отключить)    
    """
    queryset = Sensor.objects.all()

    def get_serializer_class(self):
        # Для детального просмотра используем SensorDetailSerializer
        if self.action == 'retrieve':
            return SensorDetailSerializer
        # Для всех остальных действий (list, create, update, partial_update) – SensorSerializer
        return SensorSerializer
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Method DELETE not allowed.'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@extend_schema(
    summary="Добавить измерение",
    description="Создаёт новое измерение для указанного датчика. Можно приложить изображение.",
    request=MeasurementCreateSerializer,
    responses={201: MeasurementCreateSerializer},
)
class MeasurementCreateView(generics.CreateAPIView):
    """
    View для создания нового измерения:
    POST /measurements/ 
    Принимает JSON вида:
    {
        "sensor": 1,
        "temperature": 20.5
        "image": "..." // необязательное поле
    }
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementCreateSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'data': response.data
            }, status=status.HTTP_201_CREATED
        )

