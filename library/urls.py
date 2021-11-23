from django.shortcuts import render
from .apps import APP_NAME
from . import views,apis
from django.urls import path,include


from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    
    path('books/',login_required(views.BookViews().books),name="books"),
    path('book/<int:pk>/',login_required(views.BookViews().book),name="book"),
    
    path('members/',login_required(views.MemberViews().members),name="members"),
    path('member/<int:pk>/',login_required(views.MemberViews().member),name="member"),
    
    path('lends/',login_required(views.LendViews().lends),name="lends"),
    path('lend/<int:pk>/',login_required(views.LendViews().lend),name="lend"),

    path('lend/<int:pk>/',login_required(views.BookViews().book),name="lend"),
    path('add_book/',login_required(apis.BookApi().add_book),name="add_book"),
    path('add_member/',login_required(apis.MemberApi().add_member),name="add_member"),
    path('add_lend/',login_required(apis.LendApi().lend_book),name="add_lend"),
]


