from resume.models import ResumePortfolio
from django.http import Http404
from authentication.repo import ProfileRepo
from .repo import PortfolioRepo, ResumeIndexRepo, ResumeRepo, ResumeServiceRepo
from . import constants
from core.repo import ParameterRepo
from core.views import CoreContext
from django.shortcuts import render
from .apps import APP_NAME
from django.views import View
TEMPLATE_ROOT="my_resume_en/"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)      
        if 'profile_id' in kwargs:
            resume_index=ResumeIndexRepo(request=request).resume_index(*args, **kwargs)
            context['resume_index']=resume_index
            portfolio_categories=PortfolioRepo(request=request).category_list()
            context['portfolio_categories']=portfolio_categories
            return render(request,TEMPLATE_ROOT+"index.html",context)
        raise Http404
    def portfolio(self,request,*args, **kwargs):
        context=getContext(request=request)      
        if 'pk' in kwargs:
            portfolio=PortfolioRepo(request=request).portfolio(*args, **kwargs)
            context['portfolio']=portfolio          
            return render(request,TEMPLATE_ROOT+"portfolio-details.html",context)
    def resume_service(self,request,*args, **kwargs):
        context=getContext(request=request)      
        if 'pk' in kwargs:
            resume_service=ResumeServiceRepo(request=request).resume_service(*args, **kwargs)
            context['resume_service']=resume_service          
            return render(request,TEMPLATE_ROOT+"resume-service.html",context)
    def resume(self,request,*args, **kwargs):
        context=getContext(request=request)      
        if 'pk' in kwargs:
            resume=ResumeRepo(request=request).resume(*args, **kwargs)
            context['resume']=resume          
            return render(request,TEMPLATE_ROOT+"resume.html",context)
# Create your views here.
