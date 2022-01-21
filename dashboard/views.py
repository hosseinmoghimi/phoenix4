from core.serializers import ParameterSerializer
import json
from django.http.response import Http404
from core.repo import ParameterRepo, PictureRepo
from django.shortcuts import render
from core.views import CoreContext, MessageView
from .apps import APP_NAME

TEMPLATE_ROOT="dashboard/"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']="AdminLte/layout.html"
    context['layout_parent']="material-dashboard-4/layout.html"
    return context
# Create your views here.
class BasicViews():
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)

    def parameters(self,request,*args, **kwargs):
        if not 'app_name' in kwargs:
            raise Http404
        if not request.user.has_perm("core.change_parameter"):
            mv=MessageView(title="دسترسی غیر مجاز",body="<p>شما مجوز لازم برای دسترسی به این صفحه را ندارید.</p>")
            return mv.response(request=request)
        app_name=kwargs['app_name']

        parameters=ParameterRepo(request=request,app_name=app_name).list()
        context=getContext(request=request)
        context['app_name']=app_name
        context['parameters']=parameters
        context['parameters_s']=json.dumps(ParameterSerializer(parameters,many=True).data)
        from phoenix.server_settings import apps
        my_apps=apps
        context['my_apps']=my_apps
        for my_app in my_apps:
            if my_app['name']==app_name:
                context['my_app']=my_app

        
        pictures=PictureRepo(request=request,app_name=app_name).list()
        context['pictures']=pictures
        return render(request,TEMPLATE_ROOT+"parameters.html",context)

         