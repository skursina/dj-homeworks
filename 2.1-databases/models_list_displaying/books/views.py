from datetime import date

from django.shortcuts import render
from django.http import Http404
from books.models import Book


def books_view(request, pub_date=None):
    template = 'books/books_list.html'

    previous_date = None
    next_date = None
    selected_date = None

    if pub_date:
        try:
            selected_date = date.fromisoformat(pub_date)
        except ValueError:
            raise Http404('Неверная дата публикации')
        
        books = Book.objects.filter(pub_date=selected_date).order_by('name', 'author')

        previous_date = (
            Book.objects
            .filter(pub_date__lt=selected_date)
            .order_by('-pub_date')
            .values_list('pub_date', flat=True)
            .first()
        )

        next_date = (
            Book.objects
            .filter(pub_date__gt=selected_date)
            .order_by('pub_date')
            .values_list('pub_date', flat=True)
            .first()
        )
    else:
        books = Book.objects.all().order_by('pub_date', 'name', 'author')

    context = {
        'books': books,
        'selected_date': selected_date,
        'previous_date': previous_date,
        'next_date': next_date,
    }

    return render(request, template, context)
