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
    def game1(self,request,*args, **kwargs):
        
        context=getContext(request=request)
        context['players']=PlayerRepo(request=request).list()
        context['gods']=GodRepo(request=request).list()
        roles=RoleRepo(request=request).list()
        context['roles']=roles
        context['roles_s']=json.dumps(RoleSerializer(roles,many=True).data)
        players=PlayerRepo(request=request).list()
        context['players']=players
        context['players_s']=json.dumps(PlayerSerializer(players,many=True).data)
        context['create_game_form']=CreateGameForm()
        if request.user.has_perm(APP_NAME+".add_player"):
            context['add_player_form']=AddPlayerForm()
        return render(request,TEMPLATE_ROOT+"game/game1.html",context)

    def game2(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            create_game_form=CreateGameForm(request.POST)
            if create_game_form.is_valid():
                log=30
                roles=create_game_form.cleaned_data['roles']
                players=create_game_form.cleaned_data['players']
                roles=json.loads(roles)
                players=json.loads(players)

                context=getContext(request=request)
                game=GameRepo(request=request).new_game()
                turn=0
                print(players)
                print(10*"###*#")
                players_ids=[]
                for player in players:
                    players_ids.append(player['player_id'])
                print(players_ids)
                print(10*"#$$$##*#")
                players=PlayerRepo(request=request).list().filter(id__in=players_ids)
                for role in roles:
                    for i in range(role["count"]):
                        turn+=1
                        GameRoleRepo(request=request).create(
                            role_id=role['role_id'],
                            player_id=0,
                            game_id=game.id,
                            turn=turn,
                            description=""
                        )
                    
                context['game_roles']=game.gamerole_set.all()
                context['players']=players
                context['log']=log
                return render(request,TEMPLATE_ROOT+"game/game2.html",context)
    def game(self,request,*args, **kwargs):
        game=GameRepo(request=request).game(*args, **kwargs)
        context=getContext(request=request)
        context['game']=game
        return render(request,TEMPLATE_ROOT+"game.html",context)
    def role(self,request,*args, **kwargs):
        role=RoleRepo(request=request).role(*args, **kwargs)
        context=getContext(request=request)
        context['role']=role
        return render(request,TEMPLATE_ROOT+"role.html",context)
    def games(self,request,*args, **kwargs):
        context=getContext(request=request)
        games=GameRepo(request=request).list(*args, **kwargs)
        context['games']=games
        return render(request,TEMPLATE_ROOT+"games.html",context)
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)

        roles=RoleRepo(request=request).list()
        context['roles']=roles

        players=PlayerRepo(request=request).list()
        context['players']=players

        games=GameRepo(request=request).list(*args, **kwargs)
        context['games']=games

        
        gods=GodRepo(request=request).list(*args, **kwargs)
        context['gods']=gods
       

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
   