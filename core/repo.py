from .models import *
from .constants import *
from authentication.repo import ProfileRepo
from django.db.models import Q
from .enums import ParametersEnum

class ParameterRepo:
    def __init__(self,app_name,user=None):
        self.objects=Parameter.objects.filter(Q(app_name=None)|Q(app_name=app_name))
        self.user=user
        self.app_name=app_name
    
    def change_parameter(self,parameter_id,parameter_value):
        if self.user.has_perm(APP_NAME+'.change_parameter'):
            try:
                parameter=Parameter.objects.get(pk=parameter_id)
            except:
                return None
            parameter.value_origin=parameter_value
            parameter.save()
            return parameter

    
    def set(self,name,value=None):
        # if name==ParametersEnum.LOCATION:
        #     value=value.replace('width="600"','width="100%"')
        #     value=value.replace('height="450"','height="400"') 
        if value is None:
            value=name
        olds=self.objects.filter(name=name).filter(app_name=self.app_name)
        if len(olds)>1:
            value=olds.first().value
        olds.delete()
        Parameter(name=name,value_origin=value,app_name=self.app_name).save()
    
    

    def get(self,name):
        try:
            parameter=self.objects.filter(app_name=self.app_name).get(name=name)
        except:
            self.set(name=name)
            parameter=self.objects.filter(app_name=self.app_name).get(name=name)
        return parameter
