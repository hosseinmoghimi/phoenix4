from authentication.repo import ProfileRepo
from .repo import ResumeIndexRepo
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
        selected_profile={'pk':0}  
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
            resume_index=ResumeIndexRepo(request=request).resume_index(*args, **kwargs)
            context['resume_index']=resume_index
            selected_profile=ProfileRepo(request=request,forced=1).profile(profile_id=profile_id)
            parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
            context['about_us_top']=parameter_repo.get(constants.ABOUT_US_TOP+str(selected_profile.pk))
            context['about_us_bottom']=parameter_repo.get(constants.ABOUT_US_BOTTOM+str(selected_profile.pk))
            context['skills_top']=parameter_repo.get(constants.SKILLS_TOP+str(selected_profile.pk))
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here.
