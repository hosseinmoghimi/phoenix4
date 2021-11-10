from django.shortcuts import render

# Create your views here.
from django.views import View
from core.enums import ParametersEnum

from core.repo import ParameterRepo
from .serializers import BookSerializer
from .apps import APP_NAME
from django.shortcuts import render,reverse,redirect
from .repo import BookRepo
from .forms import *
import json
from core.views import CoreContext,PageContext
TEMPLATE_ROOT="library/"
layout_parent="phoenix/layout.html"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=layout_parent
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
    context['app'] = {
        'home_url': reverse(APP_NAME+":home"),
        'tel': parameter_repo.get(ParametersEnum.TEL).value,
        'title': parameter_repo.get(ParametersEnum.TITLE).value,
    }
    return context

class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        books=BookRepo(request=request).list()
        context['books']=books
        books_s=json.dumps(BookSerializer(books,many=True).data)
        context['books_s']=books_s
        add_book_form=AddBookForm()
        context['add_book_form']=add_book_form
        return render(request,TEMPLATE_ROOT+"index.html",context)
class BookViews(View):
    def book(self,request,*args, **kwargs):
        context=getContext(request=request)
        book=BookRepo(request=request).book(*args, **kwargs)
        context.update(PageContext(request=request,page=book))
        context['book']=book
        return render(request,TEMPLATE_ROOT+"book.html",context)
