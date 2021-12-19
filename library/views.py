from django.shortcuts import render

# Create your views here.
from django.views import View
from authentication.repo import ProfileRepo
from core.enums import ParametersEnum

from core.repo import ParameterRepo
from library.enums import MemberShipLevelEnum
from .serializers import BookSerializer, LendSerializer, MemberSerializer
from .apps import APP_NAME
from django.shortcuts import render,reverse,redirect
from .repo import BookRepo, LendRepo, MemberRepo
from .forms import *
import json
from core.views import CoreContext,PageContext
TEMPLATE_ROOT="library/"
layout_parent="phoenix/layout.html"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=layout_parent
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
 
    return context

class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)

        
        books=BookRepo(request=request).list()
        context['books']=books
        books_s=json.dumps(BookSerializer(books,many=True).data)
        context['books_s']=books_s
        if request.user.has_perm(APP_NAME+".add_book"):
            add_book_form=AddBookForm()            
            context['add_book_form']=add_book_form


        
        members=MemberRepo(request=request).list()
        context['members']=members
        members_s=json.dumps(MemberSerializer(members,many=True).data)
        context['members_s']=members_s
        if request.user.has_perm(APP_NAME+".add_member"):
            add_member_form=AddMemberForm()            
            context['add_member_form']=add_member_form
            profiles=ProfileRepo(request=request).list()
            context['profiles']=profiles
        
        lends=LendRepo(request=request).list()
        context['lends']=lends
        lends_s=json.dumps(LendSerializer(lends,many=True).data)
        context['lends_s']=lends_s
        if request.user.has_perm(APP_NAME+".add_lend"):
            add_lend_form=LendBookForm()            
            context['add_lend_form']=add_lend_form


        return render(request,TEMPLATE_ROOT+"index.html",context)


class BookViews(View):
    def book(self,request,*args, **kwargs):
        context=getContext(request=request)
        book=BookRepo(request=request).book(*args, **kwargs)
        context.update(PageContext(request=request,page=book))
        context['book']=book
        return render(request,TEMPLATE_ROOT+"book.html",context)

    def books(self,request,*args, **kwargs):
        context=getContext(request=request)
        books=BookRepo(request=request).list(*args, **kwargs)
        context['books']=books
        books_s=json.dumps(BookSerializer(books,many=True).data)
        context['books_s']=books_s
        return render(request,TEMPLATE_ROOT+"books.html",context)


class MemberViews(View):
    def member(self,request,*args, **kwargs):
        context=getContext(request=request)
        member=MemberRepo(request=request).member(*args, **kwargs)
        context['member']=member
        return render(request,TEMPLATE_ROOT+"member.html",context)
    def members(self,request,*args, **kwargs):
        context=getContext(request=request)
        members=MemberRepo(request=request).list(*args, **kwargs)
        context['members']=members
        members_s=json.dumps(MemberSerializer(members,many=True).data)
        context['members_s']=members_s
        if request.user.has_perm(APP_NAME+".add_member"):
            context['add_member_form']=AddMemberForm()
            context['profiles']=ProfileRepo(request=request).list()
            context['levels']=(i[0] for i in MemberShipLevelEnum.choices)
        return render(request,TEMPLATE_ROOT+"members.html",context)






class LendViews(View):
    def lend(self,request,*args, **kwargs):
        context=getContext(request=request)
        lend=LendRepo(request=request).lend(*args, **kwargs)
        context['lend']=lend
        return render(request,TEMPLATE_ROOT+"lend.html",context)

    def lends(self,request,*args, **kwargs):
        context=getContext(request=request)
        

        books=BookRepo(request=request).list()
        context['books']=books
        books_s=json.dumps(BookSerializer(books,many=True).data)
        context['books_s']=books_s
        if request.user.has_perm(APP_NAME+".add_book"):
            add_book_form=AddBookForm()            
            context['add_book_form']=add_book_form


        
        members=MemberRepo(request=request).list()
        context['members']=members
        members_s=json.dumps(MemberSerializer(members,many=True).data)
        context['members_s']=members_s
        if request.user.has_perm(APP_NAME+".add_member"):
            add_member_form=AddMemberForm()            
            context['add_member_form']=add_member_form
            profiles=ProfileRepo(request=request).list()
            context['profiles']=profiles

        lends=LendRepo(request=request).list()
        context['lends']=lends
        lends_s=json.dumps(LendSerializer(lends,many=True).data)
        context['lends_s']=lends_s
        if request.user.has_perm(APP_NAME+".add_lend"):
            add_lend_form=LendBookForm()            
            context['add_lend_form']=add_lend_form


        return render(request,TEMPLATE_ROOT+"lends.html",context)


