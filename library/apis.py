from typing import ContextManager
from utility.persian import PersianCalendar
from .serializers import BookSerializer, LendSerializer, MemberSerializer
from core.constants import SUCCEED, FAILED
from rest_framework.views import APIView
from django.http import JsonResponse
from .repo import BookRepo, LendRepo, MemberRepo
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

    

class MemberApi(APIView):
    def add_member(self, request):
        log = 1
        context = {}
        context['result'] = FAILED
        user = request.user
        if request.method == 'POST':
            log = 2
            add_member_form = AddMemberForm(request.POST)
            if add_member_form.is_valid():
                log = 3 
                profile_id = add_member_form.cleaned_data['profile_id']
                description = add_member_form.cleaned_data['description'] 
                level = add_member_form.cleaned_data['level'] 
                member = MemberRepo(request=request).add_member(
                    profile_id=profile_id,
                    level=level,
                    description=description,
                )

                if member is not None:
                    log = 4
                    member = MemberSerializer(member).data
                    context['member'] = member
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    

class LendApi(APIView):
    def lend_book(self, request):
        log = 1
        context = {}
        context['result'] = FAILED
        user = request.user
        if request.method == 'POST':
            log = 2
            lend_book_form = LendBookForm(request.POST)
            if lend_book_form.is_valid():
                log = 3 
                member_id = lend_book_form.cleaned_data['member_id']
                book_id = lend_book_form.cleaned_data['book_id']
                description = lend_book_form.cleaned_data['description'] 
                lend = LendRepo(request=request).add_lend(
                    book_id=book_id,
                    member_id=member_id,
                    description=description,
                )

                if lend is not None:
                    log = 4
                    context['lend'] = LendSerializer(lend).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    