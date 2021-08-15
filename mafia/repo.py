from django.http import request
from django.utils import timezone
from .enums import *
from authentication.repo import ProfileRepo
from django.db.models.query_utils import Q
from .apps import APP_NAME
from .models import Action, GameRole, Player,Game,God, Role
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
    def new_game(self):
        game=Game()
        game.scenario=GameScenarioEnum.TOFANG_DAR
        game.start_date=timezone.now()
        game.god=God.objects.first()
        game.save()
        return game

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

class GameRoleRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=GameRole.objects

    def create(self,*args, **kwargs):

        game_id=kwargs['game_id'] if 'game_id' in kwargs else 0
        role_id=kwargs['role_id'] if 'role_id' in kwargs else 0
        turn=kwargs['turn'] if 'turn' in kwargs else 1
        description=kwargs['description'] if 'description' in kwargs else ""
        player_id=kwargs['player_id'] if 'player_id' in kwargs else 0

        game_role=GameRole()
        game_role.role_id=role_id
        game_role.player_id=player_id
        game_role.game_id=game_id
        game_role.turn=turn
        game_role.description=description
        game_role.save()

        return game_role


    def game_role(self, *args, **kwargs):
        
        if 'game_role_id' in kwargs:
            pk=kwargs['game_role_id']
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

class RoleRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=Role.objects
        if len(self.objects.all())==0:
            self.init_roles()

    def init_roles(self):
        Role.objects.all().delete()
        Role(priority=10,side=SideEnums.MAFIA,default_count=1,role_name="پدرخوانده").save()
        Role(priority=20,side=SideEnums.MAFIA,default_count=1,role_name="مافیای ساده").save()
        Role(priority=30,side=SideEnums.MAFIA,default_count=1,role_name="گروگان گیر").save()
        Role(priority=40,side=SideEnums.MAFIA,default_count=0,role_name="مذاکره کننده").save()
        Role(priority=50,side=SideEnums.MAFIA,default_count=0,role_name="ناتو").save()
        Role(priority=60,side=SideEnums.MAFIA,default_count=0,role_name="تروریست").save()
        Role(priority=70,side=SideEnums.CITIZEN,default_count=1,role_name="پزشک").save()
        Role(priority=80,side=SideEnums.CITIZEN,default_count=1,role_name="کاراگاه").save()
        Role(priority=90,side=SideEnums.CITIZEN,default_count=1,role_name="نگهبان").save()
        Role(priority=100,side=SideEnums.CITIZEN,default_count=1,role_name="تک تیر انداز").save()
        Role(priority=110,side=SideEnums.CITIZEN,default_count=2,role_name="شهروند ساده").save()
        Role(priority=120,side=SideEnums.CITIZEN,default_count=1,role_name="زره پوش").save()
        Role(priority=130,side=SideEnums.CITIZEN,default_count=0,role_name="نانوا").save()
        Role(priority=140,side=SideEnums.CITIZEN,default_count=0,role_name="کابوی").save()
        Role(priority=150,side=SideEnums.CITIZEN,default_count=0,role_name="ساقی").save()
    def role(self, *args, **kwargs):
        
        if 'role_id' in kwargs:
            pk=kwargs['role_id']
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

    
class ActionRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=Action.objects
        


    def action(self, *args, **kwargs):
        
        if 'action_id' in kwargs:
            pk=kwargs['action_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'game_id' in kwargs:
            game_id=kwargs['game_id']
            objects=objects.filter()
        return objects.all()

    