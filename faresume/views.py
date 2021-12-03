import json
from django.http import request
from django.shortcuts import render,reverse

from faresume.models import ResumeCategory
from faresume.seriaizers import ResumeCategorySerializer

from .apps import APP_NAME
from .repo import ResumeRepo
from django.views import View
from core.views import CoreContext

TEMPLATE_ROOT="faresume/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request):
    context=CoreContext(app_name=APP_NAME,request=request)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
 
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)

        
        resume_categories=ResumeRepo(request=request).category_list()
        context['resume_categories']=resume_categories
        resume_categories_s=json.dumps(ResumeCategorySerializer(resume_categories,many=True).data)
        context['resume_categories_s']=resume_categories_s


        return render(request,TEMPLATE_ROOT+"index.html",context)

        
    def resume(self,request,*args, **kwargs):
        context=getContext(request=request)
        resume_categories=ResumeRepo(request=request).category_list()
        context['resume_categories']=resume_categories
        resume_categories_s=json.dumps(ResumeCategorySerializer(resume_categories,many=True).data)
        context['resume_categories_s']=resume_categories_s
        return render(request,TEMPLATE_ROOT+"index.html",context)

        
    def resume_category(self,request,*args, **kwargs):
        context=getContext(request=request)
        resume_categories=ResumeRepo(request=request).category_list()
        context['resume_categories']=resume_categories
        resume_categories_s=json.dumps(ResumeCategorySerializer(resume_categories,many=True).data)
        context['resume_categories_s']=resume_categories_s
        return render(request,TEMPLATE_ROOT+"index.html",context)