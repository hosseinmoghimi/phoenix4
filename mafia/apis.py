import rest_framework
from utility.persian import PersianCalendar
from .serializers import PlayerSerializer
from core.constants import SUCCEED,FAILED
from rest_framework.views import APIView
from django.http import JsonResponse
from .repo import *
from .forms import *


class BasicApi(APIView):
    def start_game_day(self,request,*args, **kwargs):
        pass
    def start_game_night(self,request,*args, **kwargs):
        pass
    def add_all_vote(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            add_all_vote_form=AddAllVoteForm(request.POST)
            if add_all_vote_form.is_valid():
                log=3
                game_role_id=add_all_vote_form.cleaned_data['game_role_id']
                game_day_id=add_all_vote_form.cleaned_data['game_day_id']
                count=add_all_vote_form.cleaned_data['count']
                level=add_all_vote_form.cleaned_data['level']
                # profile_id=add_player_form.cleaned_data['profile_id']
                vote_repo=VoteRepo(request=request)
                result=SUCCEED
                vote_repo.clear(game_role_id=game_role_id,game_day_id=game_day_id,level=level)
                for i in range(count):
                    vote=vote_repo.add_vote(game_role_id=game_role_id,game_day_id=game_day_id,level=level)
                    if vote is None:
                        result=FAILED
                return JsonResponse({'result':result})
        return JsonResponse({'result':FAILED,'log':log})
    
    def new_game(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            add_player_form=AddPlayerForm(request.POST)
            if add_player_form.is_valid():
                log=3
                username=add_player_form.cleaned_data['username']
                password=add_player_form.cleaned_data['password']
                first_name=add_player_form.cleaned_data['first_name']
                last_name=add_player_form.cleaned_data['last_name']
                mobile=add_player_form.cleaned_data['mobile']
                email=add_player_form.cleaned_data['email']
                address=add_player_form.cleaned_data['address']
                bio=add_player_form.cleaned_data['bio']
                # profile_id=add_player_form.cleaned_data['profile_id']
                player=PlayerRepo(request=request).add_player(
                    # profile_id=profile_id,
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    bio=bio,
                    mobile=mobile,
                    address=address,
                    email=email,
                    )
                
                if player is not None:
                    log=4
                    player=PlayerSerializer(player).data
                    return JsonResponse({'result':SUCCEED,'player':player})
        return JsonResponse({'result':FAILED,'log':log})
    
    def add_player(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            add_player_form=AddPlayerForm(request.POST)
            if add_player_form.is_valid():
                log=3
                username=add_player_form.cleaned_data['username']
                password=add_player_form.cleaned_data['password']
                first_name=add_player_form.cleaned_data['first_name']
                last_name=add_player_form.cleaned_data['last_name']
                mobile=add_player_form.cleaned_data['mobile']
                email=add_player_form.cleaned_data['email']
                address=add_player_form.cleaned_data['address']
                bio=add_player_form.cleaned_data['bio']
                # profile_id=add_player_form.cleaned_data['profile_id']
                player=PlayerRepo(request=request).add_player(
                    # profile_id=profile_id,
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    bio=bio,
                    mobile=mobile,
                    address=address,
                    email=email,
                    )
                
                if player is not None:
                    log=4
                    player=PlayerSerializer(player).data
                    return JsonResponse({'result':SUCCEED,'player':player})
        return JsonResponse({'result':FAILED,'log':log})
    