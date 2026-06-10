from django.shortcuts import render, redirect, get_object_or_404
from phones.models import Phone

SORT_MAP = {
    'name': 'name',
    'min_price': 'price',
    'max_price': '-price',
    }


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort', 'name')
    order_by = SORT_MAP.get(sort)

    phones = Phone.objects.all()
    if order_by:
        phones = phones.order_by(order_by)

    context = {
        'phones': phones,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'

    phone = get_object_or_404(Phone, slug=slug)
    context = {
        'phone': phone,
    }
    return render(request, template, context)
