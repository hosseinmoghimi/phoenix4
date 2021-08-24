from resume.forms import AddResumeFactForm, AddResumeSkillForm
from resume.enums import LanguageEnum, ResumeItemEnum
from resume.utils import AdminUtility
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
def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    language=LanguageEnum.ENGLISH
    if 'language' in kwargs:
        language=kwargs['language']
    context['language']=language
    context['admin_utility']=AdminUtility(request=request)
    context['title']='Resume'
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request,*args,**kwargs)
        # language=LanguageEnum.ENGLISH
        # if 'language' in kwargs:
        #     language=kwargs['language']
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
            resume_index=ResumeIndexRepo(request=request,*args, **kwargs).resume_index(profile_id=profile_id)
            context['resume_index']=resume_index
            parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
            context['location']=parameter_repo.get(name='location')
            context['email']=parameter_repo.get(name='email')
            context['call']=parameter_repo.get(name='call')
            context['resume_index']=resume_index
            context['title']=resume_index.title


            portfolio_categories=PortfolioRepo(request=request).category_list()
            context['portfolio_categories']=portfolio_categories
            profile=ProfileRepo(request=request).me
            if profile.id==profile_id or request.user.has_perm(APP_NAME+"change_resumeindex"):
                #user can change resume
                context['add_resume_fact_form']=AddResumeFactForm()
                context['add_resume_skill_form']=AddResumeSkillForm()
                # context['resume_item_enums']=(i[0] for i in ResumeItemEnum.choices)
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
