from pathlib import Path
import csv

from django.core.management.base import BaseCommand
from django.conf import settings    
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        csv_path = Path(settings.BASE_DIR)/'phones.csv'

        with csv_path.open('r', encoding='utf-8') as file:
            phones = csv.DictReader(file, delimiter=';')

            for phone in phones:
                Phone.objects.update_or_create(
                    id=int(phone['id']), 
                    defaults={
                        'name': phone['name'], 
                        'price': int(phone['price']),
                        'image': phone['image'], 
                        'release_date': phone['release_date'], 
                        'lte_exists': phone['lte_exists'] == 'True',
                        }
                )