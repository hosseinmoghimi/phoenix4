from os import scandir
from rest_framework.views import APIView
from .serializers import *
from django.http import JsonResponse
from core.constants import FAILED,SUCCEED
from .apps import APP_NAME
from .repo import *
from .forms import *




from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import AllowAny


from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


   
@api_view(['GET','POST'])
@authentication_classes([CsrfExemptSessionAuthentication,BasicAuthentication])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def add_log_from_client(request):
    context={}
    feeder_sn=request.data['feeder_sn']
    feeder_pin=request.data['feeder_pin']
    register=request.data['register']
    command=request.data['command']

    context['feeder_sn']=feeder_sn
    context['feeder_pin']=feeder_pin
    context['register']=register
    context['command']=command
    res=LogRepo().add_log_from_client(feeder_sn=feeder_sn,feeder_pin=feeder_pin,register=register,command=command)
    
    return JsonResponse(res)

@permission_classes([AllowAny])
class BasicApi(APIView):
    def export(self,request,*args, **kwargs):
        context={}

        context['feeders']=FeederSerializer(Feeder.objects.all(),many=True).data
        context['relays']=RelaySerializerForExportData(Relay.objects.order_by('feeder_id'),many=True).data
        context['commands']=CommandSerializerForExportData(Command.objects.order_by('relay_id'),many=True).data
        context['scenarioes']=ScenarioSerializerForExportData(Scenario.objects.all(),many=True).data
        return JsonResponse(context)
    def get_logs(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            get_log_form=GetLogForm(request.POST)
            if get_log_form.is_valid():
                log=3
                page=get_log_form.cleaned_data['page']
                per_page=get_log_form.cleaned_data['per_page']
                logs=LogRepo(request=request).page(page=page,per_page=per_page)
                context['logs']=LogSerializer(logs,many=True).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

     
    def get_logs(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            get_log_form=GetLogForm(request.POST)
            if get_log_form.is_valid():
                log=3
                page=get_log_form.cleaned_data['page']
                per_page=get_log_form.cleaned_data['per_page']
                logs=LogRepo(request=request).page(page=page,per_page=per_page)
                context['logs']=LogSerializer(logs,many=True).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def run_scenario(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            run_scenario_form=RunScenarionForm(request.POST)
            if run_scenario_form.is_valid():
                log=3
                scenario_id=run_scenario_form.cleaned_data['scenario_id']
                scenario_pin=run_scenario_form.cleaned_data['pin']
                done=ScenarioRepo(request=request).run_scenario(scenario_id=scenario_id,scenario_pin=scenario_pin)
                context['result']=done['result']
        context['log']=log
        return JsonResponse(context)
    
    def execute_command(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            execute_command_form=ExecuteCommandForm(request.POST)
            if execute_command_form.is_valid():
                log=3
                command_id=execute_command_form.cleaned_data['command_id']
                relay_pin=execute_command_form.cleaned_data['pin']
                response=CommandRepo(request=request).execute_command(command_id=command_id,relay_pin=relay_pin)  
                if response['result']==SUCCEED:
                    context['registers']=response['registers']
                context['result']=response['result']
        context['log']=log
        return JsonResponse(context)