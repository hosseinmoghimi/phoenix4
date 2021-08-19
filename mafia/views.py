from django.shortcuts import redirect, render
from django.views import View
from .serializers import GameRoleSerializer, RoleSerializer,PlayerSerializer
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
        context['scenarioes']=(i[0] for i in GameScenarioEnum.choices)
        context['roles_s']=json.dumps(RoleSerializer(roles,many=True).data)
        players=PlayerRepo(request=request).list()
        context['players']=players
        context['players_s']=json.dumps(PlayerSerializer(players,many=True).data)
        context['create_game_form']=CreateGameForm()
        if request.user.has_perm(APP_NAME+".add_player"):
            context['add_player_form']=AddPlayerForm()
        return render(request,TEMPLATE_ROOT+"game/game1.html",context)

    def shuffle_game(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            print(10*"#222#")
            log=2
            shuffle_game_form=ShuffleGameForm(request.POST)
            if shuffle_game_form.is_valid():
                log=3
                game_id=shuffle_game_form.cleaned_data['game_id']
                game=GameRepo(request=request).game(game_id=game_id)
                if game is not None:
                    game_roles=game.game_roles()
                    players_ids=[]
                    for game_role in game_roles:
                        player_id=game_role.player.id
                        players_ids.append(player_id)
                    from utility.random import shuffle_array
                    players_ids=shuffle_array(players_ids)

                    i=0
                    for game_role in game_roles:
                        game_role.player_id=players_ids[i]
                        i+=1
                        game_role.save()

                    return redirect(game.get_absolute_url())

    def game2(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            print(10*"#222#")
            log=2
            create_game_form=CreateGameForm(request.POST)
            if create_game_form.is_valid():
                print(10*"#333#")
                log=30
                scenario=create_game_form.cleaned_data['scenario']
                god_id=create_game_form.cleaned_data['god_id']
                roles=create_game_form.cleaned_data['roles']
                players=create_game_form.cleaned_data['players']
                roles=json.loads(roles)
                players=json.loads(players)
                context=getContext(request=request)
                print(god_id)
                print(100*"#")
                game=GameRepo(request=request).new_game(god_id=god_id,scenario=scenario)
                turn=0
                players_ids=[]
                for player in players:
                    players_ids.append(player['player_id'])
                players=PlayerRepo(request=request).list().filter(id__in=players_ids)
                players_ids_2=[]
                a=-1
                from utility.random import shuffle_array
                players_ids_2=shuffle_array(players_ids)
                for role in roles:
                    a+=1
                    for i in range(role["count"]):
                        turn+=1
                        GameRoleRepo(request=request).create(
                            role_id=role['role_id'],
                            player_id=players_ids_2[a],
                            game_id=game.id,
                            turn=turn,
                            description=""
                        )
                    
                context['game_roles']=game.gamerole_set.all()
                context['game_roles_s']=json.dumps(GameRoleSerializer(game.game_roles(),many=True).data)
                context['players']=players
                context['players_s']=json.dumps(PlayerSerializer(players,many=True).data)
                context['log']=log
                context['game']=game
                # return render(request,TEMPLATE_ROOT+"game/game2.html",context)
                return redirect(game.get_absolute_url())
    def game_role(self,request,*args, **kwargs):
        game_role=GameRoleRepo(request=request).game_role(*args, **kwargs)
        context=getContext(request=request)
        context['game_role']=game_role
        return render(request,TEMPLATE_ROOT+"game-role.html",context)
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
        context['games']=games[:10]

        
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
   