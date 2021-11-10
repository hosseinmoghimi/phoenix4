from typing import ContextManager
from utility.persian import PersianCalendar
from .serializers import BookSerializer
from core.constants import SUCCEED, FAILED
from rest_framework.views import APIView
from django.http import JsonResponse
from .repo import BookRepo
from .forms import *


class BookApi(APIView):
    def add_book(self, request):
        log = 1
        context = {}
        context['result'] = FAILED

        user = request.user
        if request.method == 'POST':
            log = 2
            add_book_form = AddBookForm(request.POST)
            if add_book_form.is_valid():
                log = 3 
                title = add_book_form.cleaned_data['title'] 
                price = add_book_form.cleaned_data['price'] 
                year = add_book_form.cleaned_data['year'] 
                shelf = add_book_form.cleaned_data['shelf'] 
                col = add_book_form.cleaned_data['col'] 
                row = add_book_form.cleaned_data['row'] 
                description = add_book_form.cleaned_data['description'] 
                book = BookRepo(request=request).add_book(
                    title=title,
                    year=year,
                    price=price,                  
                    description=description,
                    row=row,
                    col=col,
                    shelf=shelf
                )

                if book is not None:
                    log = 4
                    book = BookSerializer(book).data
                    context['book'] = book
                    context['result'] = SUCCEED
        return JsonResponse(context)

    