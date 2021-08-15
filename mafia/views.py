from mafia.models import Player
from django.shortcuts import render
from django.views import View
from .serializers import RoleSerializer,PlayerSerializer
from .repo import * 
from .forms import * 
from core.views import CoreContext
from .apps import APP_NAME
import json
TEMPLATE_ROOT='mafia/'

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)    
    return context

class BasicViews(View):
    def new_game(self,request,*args, **kwargs):
        
        context=getContext(request=request)
        context['players']=PlayerRepo(request=request).list()
        context['gods']=GodRepo(request=request).list()
        roles=RoleRepo(request=request).list()
        context['roles']=roles
        context['create_game_by_roles_form']=CreateGameByRolesForm()
        context['roles_s']=json.dumps(RoleSerializer(roles,many=True).data)
        if request.user.has_perm(APP_NAME+".add_player"):
            context['add_player_form']=AddPlayerForm()
        return render(request,TEMPLATE_ROOT+"new-game.html",context)

    def create_game_by_roles(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            create_game_by_roles_form=CreateGameByRolesForm(request.POST)
            if create_game_by_roles_form.is_valid():
                log=30
                game_roles=create_game_by_roles_form.cleaned_data['game_roles']
                roles=json.loads(game_roles)

                context=getContext(request=request)
                game=GameRepo(request=request).new_game()
                game_roles=[]
                turn=0
                for role in roles:
                    turn+=1
                    game_role=GameRoleRepo(request=request).create(
                        role=RoleRepo(request=request).role(pk=role.id),
                        player=None,
                        game=game,
                        turn=turn,
                        description=""
                    )
                
                context['game_roles']=game.gamerole_set.all()


        context['log']=log
        return render(request,TEMPLATE_ROOT+"game.html",context)

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
