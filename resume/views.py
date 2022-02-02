import json
from core.models import PageComment
from projectmanager.repo import ServiceRepo
import resume

from resume.serializers import ResumeFactSerializer, ResumeSkillSerializer
from .apps import APP_NAME
from .enums import LanguageEnum, ResumeItemEnum, languageToIndex
from .forms import AddResumeFactForm, AddResumeSkillForm
from .models import ResumePortfolio
from .repo import PortfolioRepo, ResumeIndexRepo, ResumeRepo, ResumeServiceRepo
from .utils import AdminUtility


from django.http import Http404
from authentication.repo import ProfileRepo
from core.repo import ParameterRepo
from core.views import CoreContext, PageContext
from django.shortcuts import render
from django.views import View


TEMPLATE_ROOT = "my_resume_en/"
def get_resume_index_context(request,*args, **kwargs):
    resume_index=None
    if 'resume_index' in kwargs:
        resume_index=kwargs['resume_index']
    else:
        resume_index=ResumeIndexRepo(request=request).resume_index(*args, **kwargs)
    if resume_index is None:
        return


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    language = LanguageEnum.ENGLISH
    if 'language' in kwargs:
        language = kwargs['language']
    context['language'] = language
    if language == LanguageEnum.ENGLISH:
        TEMPLATE_ROOT = "my_resume_en/"
    if language == LanguageEnum.FARSI:
        TEMPLATE_ROOT = "my_resume_fa/"
    context['admin_utility'] = AdminUtility(request=request)
    context['title'] = 'Resume'
    context['TEMPLATE_ROOT'] = TEMPLATE_ROOT
    return context
class PortfolioViews(View):
    def portfolio(self,request,*args, **kwargs):
        portfolio=PortfolioRepo(request=request).portfolio(*args, **kwargs)
        context = getContext(request=request,language=portfolio.resume_index.language)
        context['portfolio']=portfolio
        if str(portfolio.resume_index.language)==str(LanguageEnum.FARSI):
            TEMPLATE_ROOT="my_resume_fa/" 
        if str(portfolio.resume_index.language)==str(LanguageEnum.ENGLISH):
            TEMPLATE_ROOT="my_resume_en/" 
        context['layout_parent']='material-kit-pro/layout.html'
        context.update(PageContext(request=request,page=portfolio))
        return render(request, TEMPLATE_ROOT+"portfolio.html", context)
class ServiceViews(View):
    def service(self,request,*args, **kwargs):
        service=ServiceRepo(request=request).service(*args, **kwargs)
        context = getContext(request=request,language=service.resume_index.language)
        context['service']=service
        if str(service.resume_index.language)==str(LanguageEnum.FARSI):
            TEMPLATE_ROOT="my_resume_fa/" 
        if str(service.resume_index.language)==str(LanguageEnum.ENGLISH):
            TEMPLATE_ROOT="my_resume_en/" 
        context['layout_parent']='material-kit-pro/layout.html'
        context.update(PageContext(request=request,page=service))
        return render(request, TEMPLATE_ROOT+"service.html", context)

class BasicViews(View):

    def home(self, request, *args, **kwargs):
        if 'profile_id' not in kwargs:
            raise Http404
        language = LanguageEnum.ENGLISH
        # language=LanguageEnum.ENGLISH
        if 'language_index' in kwargs:
                language = languageToIndex(index=kwargs['language_index'])
        context = getContext(request=request,language=language)
        profile_id = kwargs['profile_id']
        resume_index = ResumeIndexRepo(
            request=request,language=language, *args, **kwargs).resume_index(profile_id=profile_id)
        context['resume_index'] = resume_index
        parameter_repo = ParameterRepo(request=request, app_name=APP_NAME)
        context['location'] = parameter_repo.get(name='location')
        context['email'] = parameter_repo.get(name='email')
        context['call'] = parameter_repo.get(name='call')
        context['resume_index'] = resume_index
        context['title'] = resume_index.title


        skills=resume_index.resumeskill_set.order_by('priority')
        context['skills']=skills
        context['skills_s']=json.dumps(ResumeSkillSerializer(skills,many=True).data)


        facts=resume_index.resumefact_set.order_by('priority')
        context['facts']=facts
        context['facts_s']=json.dumps(ResumeFactSerializer(facts,many=True).data)

        context['portfolios'] = resume_index.resumeportfolio_set.all()

        # portfolio_categories = PortfolioRepo(request=request).category_list()
        # context['portfolio_categories'] = portfolio_categories
        portfolio_filters = PortfolioRepo(request=request).filter_list()
        context['portfolio_filters'] = portfolio_filters
        profile = ProfileRepo(request=request).me
        if profile is not None and (profile.id == profile_id or request.user.has_perm(APP_NAME+"change_resumeindex")):
            # user can change resume
            context['add_resume_fact_form'] = AddResumeFactForm()
            context['add_resume_skill_form'] = AddResumeSkillForm()
            # context['resume_item_enums']=(i[0] for i in ResumeItemEnum.choices)
        TEMPLATE_ROOT = context['TEMPLATE_ROOT']
        return render(request, TEMPLATE_ROOT+"/index.html", context)

    # def portfolio(self, request, *args, **kwargs):
    #     context = getContext(request=request)
    #     if 'pk' in kwargs:
    #         portfolio = PortfolioRepo(
    #             request=request).portfolio(*args, **kwargs)
    #         context['portfolio'] = portfolio
    #         return render(request, TEMPLATE_ROOT+"portfolio-details.html", context)

    # def resume_service(self, request, *args, **kwargs):
    #     context = getContext(request=request)
    #     if 'pk' in kwargs:
    #         resume_service = ResumeServiceRepo(
    #             request=request).resume_service(*args, **kwargs)
    #         context['resume_service'] = resume_service
    #         return render(request, TEMPLATE_ROOT+"resume-service.html", context)


    def resume_print(self, request, *args, **kwargs):
        
        language = LanguageEnum.ENGLISH
        # language=LanguageEnum.ENGLISH
        if 'language_index' in kwargs:
                language = languageToIndex(index=kwargs['language_index'])
        context = getContext(request=request,language=language)
        
        resume_index = ResumeIndexRepo(
            request=request).resume_index(*args, **kwargs)
        context['resume_index'] = resume_index
        parameter_repo = ParameterRepo(request=request, app_name=APP_NAME)
        context['location'] = parameter_repo.get(name='location')
        context['email'] = parameter_repo.get(name='email')
        context['call'] = parameter_repo.get(name='call')
        context['resume_index'] = resume_index
        context['title'] = resume_index.title
        context['portfolios'] = resume_index.resumeportfolio_set.all()


        skills=resume_index.resumeskill_set.order_by('priority')
        context['skills']=skills


        facts=resume_index.resumefact_set.order_by('priority')
        context['facts']=facts

        # portfolio_categories = PortfolioRepo(request=request).category_list()
        # context['portfolio_categories'] = portfolio_categories
        portfolio_filters = PortfolioRepo(request=request).filter_list()
        context['portfolio_filters'] = portfolio_filters
        profile = ProfileRepo(request=request).me
        if resume_index.language==LanguageEnum.ENGLISH:
            TEMPLATE_ROOT = "my_resume_en/"
        if resume_index.language==LanguageEnum.FARSI:
            TEMPLATE_ROOT = "my_resume_fa/"
        return render(request, TEMPLATE_ROOT+"resume-print.html", context)


    def resume(self, request, *args, **kwargs):
        context = getContext(request=request)
        if 'pk' in kwargs:
            resume = ResumeRepo(request=request).resume(*args, **kwargs)
            context['resume'] = resume
            return render(request, TEMPLATE_ROOT+"resume.html", context)
# Create your views here.
