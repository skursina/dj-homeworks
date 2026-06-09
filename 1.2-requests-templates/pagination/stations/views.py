from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings

import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    stations = load_stations(request)

    page_number = request.GET.get('page', 1)
    
    paginate = Paginator(stations, 10)
    page = paginate.get_page(page_number)
    
    context = {
        'bus_stations': page.object_list,
        'page': page,
    }

    return render(request, 'stations/index.html', context)


def load_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        
        return reader