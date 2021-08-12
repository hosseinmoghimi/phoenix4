from mafia.models import Player
from django.shortcuts import render
from django.views import View
from .repo import * 
from .forms import * 
from core.views import CoreContext
from .apps import APP_NAME

TEMPLATE_ROOT='mafia/'

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)    
    return context

class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['players']=PlayerRepo(request=request).list()
        context['gods']=GodRepo(request=request).list()
        context['games']=GameRepo(request=request).list()
        if request.user.has_perm(APP_NAME+".add_player"):
            context['add_player_form']=AddPlayerForm()
        return render(request,TEMPLATE_ROOT+"index.html",context)


    def player(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['player']=PlayerRepo(request=request).player(*args, **kwargs)
        return render(request,TEMPLATE_ROOT+"player.html",context)
    def god(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['god']=GodRepo(request=request).god(*args, **kwargs)
        return render(request,TEMPLATE_ROOT+"god.html",context)
    def game(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['game']=GameRepo(request=request).game(*args, **kwargs)
        return render(request,TEMPLATE_ROOT+"game.html",context)
