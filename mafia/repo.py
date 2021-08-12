from django.http import request
from django.utils import timezone
from .enums import *
from authentication.repo import ProfileRepo
from django.db.models.query_utils import Q
from .apps import APP_NAME
from .models import Player,Game,God
from utility.persian import PersianCalendar

class PlayerRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=Player.objects

    def add_player(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_player"):
            return None
        player=Player()
        if 'profile_id' in kwargs and kwargs['profile_id']>0:
            player.profile=ProfileRepo(request=self.request).profile(profile_id=kwargs['profile_id'])
            player.save()
            return player
        profile=ProfileRepo(request=self.request).register(*args, **kwargs)
        player.profile=profile
        player.save()
        return player


    def player(self, *args, **kwargs):
        if 'player_id' in kwargs:
            pk=kwargs['player_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(profile__first_name__contains=kwargs['search_for'])
        return objects.all()

    


    
class GameRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=Game.objects


    def game(self, *args, **kwargs):
        
        if 'game_id' in kwargs:
            pk=kwargs['game_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(profile__first_name__contains=kwargs['search_for'])
        return objects.all()

    



    
class GodRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=God.objects
        


    def god(self, *args, **kwargs):
        
        if 'god_id' in kwargs:
            pk=kwargs['god_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    

    def list(self, *args, **kwargs):
        objects = self.objects
        return objects.all()

    