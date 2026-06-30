import os

from django.utils import timezone
from django.utils.text import slugify
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


def measurement_image_path(instance, filename):
    ext = filename.split('.')[-1]
    sensor_id = instance.sensor.id if instance.sensor else 'unknown'
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    safe_sensor_id = slugify(str(sensor_id))
    new_filename = f"sensor_{safe_sensor_id}_{timestamp}.{ext}"

    return os.path.join('measurement_photos', new_filename)


class Sensor(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField(validators=[MinValueValidator(-50.0), MaxValueValidator(50.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=measurement_image_path, blank=True, null=True)

    def __str__(self):
        return f"{self.sensor.name} - {self.temperature}C at {self.created_at}"

