from authentication.repo import ProfileRepo
from core.constants import FAILED, SUCCEED
from core import repo as CoreRepo
from .models import *
import requests
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F

class LogRepo():
    def __init__(self,*args,**kwargs):
        
        
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Log.objects
        self.profile=ProfileRepo(user=self.user).me
    def add_log_from_client(self,feeder_sn,feeder_pin,register,command):
        try:
            feeder=Feeder.objects.filter(serial_no=feeder_sn).get(feeder_pin=feeder_pin)
        except:
            return {'result':FAILED,'message':'no feeder'}
        try:
            relay=feeder.relay_set.get(register=register)
        except:
            return {'result':FAILED,'message':'no relay'}
        try:
            command=relay.command_set.get(value=command)
        except:
            return {'result':FAILED,'message':'no command'}
        log=Log(title=command.name,command=command,feeder=feeder,relay=relay)
        log.save()
        return {'result':SUCCEED}


    def list(self,*args, **kwargs):
        return self.objects.all()
    def page(self,page=1,per_page=20):
        start=len(self.objects.all())-(per_page*page)+1
        end=start+per_page-1
        a=self.objects
        a=a.filter(id__lte=end)
        a=a.filter(id__gte=start)
        a=a.order_by('-id')
        return a
    def log(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            pass
class ScenarioRepo():
    def __init__(self,*args,**kwargs):
        
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Scenario.objects
        self.profile=ProfileRepo(user=self.user).me

    def list(self,*args, **kwargs):
        return self.objects.all()

    def scenario(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            pass
    def run_scenario(self,scenario_id,scenario_pin=None):
        scenario=Scenario.objects.get(pk=scenario_id)        
        feeder_repo=FeederRepo(self.user)
        if scenario is None:
            return {'result':FAILED}
        if scenario is not None:
            scenario_pin= scenario_pin if scenario.is_protected else scenario.pin
            if self.profile in scenario.profiles.all() and scenario.scenario_pin==scenario_pin:
                Log(title=scenario.name,scenario=scenario,profile=self.profile).save()
                for command in scenario.commands.all():
                    if self.profile in command.profiles.all():
                        relay_pin=command.relay.relay_pin
                        CommandRepo(user=self.user).execute_command(command_id=command.id,relay_pin=relay_pin)
                return {'result':SUCCEED}
        for feeder in feeder_repo.list():
            feeder_repo.get_state(feeder.id)




class FeederRepo():
    def __init__(self,*args,**kwargs):
        
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Feeder.objects
        self.profile=ProfileRepo(user=self.user).me

    def list(self,*args, **kwargs):
        return self.objects.all()

    def feeder(self,*args, **kwargs):
        pk=0
        if 'feeder_id' in kwargs:
            pk=kwargs['feeder_id']
        elif 'id' in kwargs:
            pk=kwargs['id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        try:
            return self.objects.get(pk=pk)
        except:
            return None
    def get_state(self,*args, **kwargs):
        if 'feeder_id' in kwargs:
            feeder=self.feeder(kwargs['feeder_id'])
        elif 'feeder' in kwargs:
            feeder=kwargs['feeder']
        else:
            return
        payload={}
        from .client import handleGetStatus_url
        url=f'http://{feeder.ip}:{feeder.port}/'+handleGetStatus_url
        response=requests.get(url,payload)
        # return {'response':response.json(),'url':url}
        registers=response.json()['registers']
        for register in registers:
            register_no=int(register['register'])
            state=(True if int(register['state'])==1 else False)
            relay=Relay.objects.filter(feeder=feeder).filter(register=register_no).first()
            relay.current_state=state
            relay.save()                
        return (registers,feeder)
  


class RelayRepo():
    def __init__(self,*args,**kwargs):
        
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Relay.objects
        self.profile=ProfileRepo(user=self.user).me

    def list(self,*args, **kwargs):
        return self.objects.all()

    def relay(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None

class CommandRepo():
    def __init__(self,*args, **kwargs):
        
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Command.objects
        self.profile=ProfileRepo(user=self.user).me
    def my_commands(self,*args, **kwargs):
        commands=self.profile.command_set.all()
        if 'feeder' in kwargs:
            feeder=kwargs['feeder']
            relays=feeder.relay_set.all()
            commands=commands.filter(relay__in=relays)   
        elif 'feeder_id' in kwargs:
            feeder_id=kwargs['feeder_id']
            feeder=FeederRepo(self.user).feeder(feeder_id)
            relays=feeder.relay_set.all()
            commands=commands.filter(relay__in=relays)            
        elif 'relay_id' in kwargs:
            relay_id=kwargs['relay_id']
            commands=commands.filter(relay_id=relay_id)
        else:
            return []
        return commands

    def list(self,*args, **kwargs):
        return self.objects.all()
        
    def execute_command(self,command_id,relay_pin=None):
        command=Command.objects.get(pk=command_id)
        if command is not None:                 
            if not self.profile in command.profiles.all():
                return {'result':FAILED}
           
            if self.profile in command.profiles.all():
                ip=command.relay.feeder.ip
                relay_pin= relay_pin if command.relay.is_protected else command.relay.pin
                if relay_pin==command.relay.relay_pin:
                    port=command.relay.feeder.port
                    register=command.relay.register
                    command_value=command.value
                    payload={'register':register,'command':command_value,'key':relay_pin,'pin':relay_pin}
                    from .client import handleExecuteCommand_url
                    url=f'http://{ip}:{port}/'+handleExecuteCommand_url
                    from core.constants import FAILED,SUCCEED
                    try:
                        response=requests.post(url,payload)
                    except:
                        Log(title=command.name,feeder=command.relay.feeder,relay=command.relay,profile=self.profile,command=command,succeed=False).save()
                        return {'result':FAILED}
                    registers=response.json()['registers']
                    relays=command.relay.feeder.relay_set.all()
                    for register in registers:
                        register_no=int(register['register'])
                        relay=relays.get(register=register_no)
                        if register_no==command.relay.register:
                            pass
                        state=int(register['state'])==1
                        relay.current_state=state
                        relay.save()
                    Log(title=command.name,feeder=command.relay.feeder,relay=command.relay,profile=self.profile,command=command,succeed=True).save()
                    return {'registers':registers,'result':SUCCEED}
            Log(title=command.name,feeder=command.relay.feeder,relay=command.relay,profile=self.profile,command=command,succeed=False).save()
        return {'result':FAILED}

    def command(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None