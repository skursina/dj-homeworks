from django.contrib import admin
from .models import Sensor, Measurement

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)  


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'sensor', 'temperature', 'created_at', 'image_preview')
    list_filter = ('sensor', 'created_at')
    search_fields = ('sensor__name', 'temperature')
    readonly_fields = ('created_at',)  # чтобы не редактировали время вручную
    fields = ('sensor', 'temperature', 'image', 'created_at')  # порядок полей

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px;" />'
        return '-'
    image_preview.short_description = 'Превью'
    image_preview.allow_tags = True