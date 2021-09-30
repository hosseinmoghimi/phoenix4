from django.shortcuts import render
from core.views import CoreContext
from school.repo import SchoolRepo
from .apps import APP_NAME
from django.views import View

TEMPLATE_FOLDER="school/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        schools=SchoolRepo(request=request).list(*args, **kwargs)
        context['schools']=schools
        return render(request,TEMPLATE_FOLDER+"index.html",context)


class SchoolViews(View):
    def school(self,request,*args, **kwargs):
        context=getContext(request=request)
        school=SchoolRepo(request=request).school(*args, **kwargs)
        context['school']=school
        return render(request,TEMPLATE_FOLDER+"school.html",context)