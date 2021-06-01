from .models import *
from .constants import *
from authentication.repo import ProfileRepo
from django.db.models import Q
from .enums import ParametersEnum
from authentication.repo import ProfileRepo
class BasicPageRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=BasicPage.objects
    def add_page(self,title,*args, **kwargs):
        new_page=BasicPage(title=title)
        new_page.title=title
        if 'parent_id' in kwargs:
            new_page.parent_id=kwargs['parent_id']
            new_page.parent_id=kwargs['parent_id']
        new_page.save()
        new_page.app_name=new_page.parent.app_name
        new_page.class_name=new_page.parent.class_name
        new_page.save()
        return new_page

    def page(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'project_id' in kwargs:
            return self.objects.filter(pk=kwargs['project_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])        
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects.all()


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
