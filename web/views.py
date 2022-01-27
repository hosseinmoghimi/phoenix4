
from authentication.views import ProfileContext
from core.enums import PictureNameEnums
from core.repo import ParameterRepo, PictureRepo
from django.shortcuts import render
from .repo import *
from django.views import View
from core.views import CoreContext, PageContext
from .enums import ParameterEnum
from .forms import *


LAYOUT_PARENT='material-kit-pro/layout.html'
TEMPLATE_ROOT="web/"

def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    context['search_form'] = SearchForm()
    context['navbar'] = APP_NAME+"/includes/nav-bar.html"
    return context

class BasicViews(View):
    
    
    def search(self, request, *args, **kwargs):
        context = getContext(request)
        log = 1
        if request.method == 'POST':
            log += 1
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                log += 1
                search_for = search_form.cleaned_data['search_for']
                context['search_for'] = search_for
                context['blogs'] = BlogRepo(
                    request=request).list(search_for=search_for) 
                context['crypto_tokens'] = CryptoTokenRepo(
                    request=request).list(search_for=search_for) 
                context['log'] = log
                context['header_image'] = PictureRepo(
                    request=request, app_name=APP_NAME).picture(name=PictureNameEnums.SEARCH_HEADER)

                return render(request, TEMPLATE_ROOT+"search.html", context)
        return BasicViews().home(request=request)



    def contact(self,request,*args, **kwargs):
        context=getContext(request)
        return render(request,TEMPLATE_ROOT+"contact.html",context)
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        context['body_class']="sections-page"

        blogs=BlogRepo(request=request).list(for_home=True,*args, **kwargs)
        context['blogs']=blogs

        our_works=OurWorkRepo(request=request).list(for_home=True,*args, **kwargs)
        context['blogs']=blogs

        teams=OurTeamRepo(request=request).list(for_home=True,*args, **kwargs)
        context['teams']=teams

        sliders=CarouselRepo(request=request).list(for_home=True,app_name=APP_NAME,*args, **kwargs)
        context['sliders']=sliders


        features=FeatureRepo(request=request).list(for_home=True,*args, **kwargs)
        context['features']=features


        our_works=OurWorkRepo(request=request).list(for_home=True,*args, **kwargs)
        context['our_works']=our_works

        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        context['blog_title_param']=parameter_repo.parameter(name=ParameterEnum.BlogsTitle)
        context['blog_description_param']=parameter_repo.parameter(name=ParameterEnum.BlogsDescription)

        context['feature_title_param']=parameter_repo.parameter(name=ParameterEnum.FeatureTitle)
        context['feature_description_param']=parameter_repo.parameter(name=ParameterEnum.FeatureDescription)
        
        context['ourwork_pretitle_param']=parameter_repo.parameter(name=ParameterEnum.OurWorksPreTitle)
        context['ourwork_title_param']=parameter_repo.parameter(name=ParameterEnum.OurWorksTitle)
        context['ourwork_description_param']=parameter_repo.parameter(name=ParameterEnum.OurWorksDescription)

        context['ourteam_title_param']=parameter_repo.parameter(name=ParameterEnum.OurTeamTitle)
        context['ourteam_description_param']=parameter_repo.parameter(name=ParameterEnum.OurTeamDescription)

        param_repo=ParameterRepo(request=request)
        context['office_address']=parameter_repo.parameter(name=ParameterEnum.OFFICE_ADDRESS).value
        context['office_tel']=parameter_repo.parameter(name=ParameterEnum.OFFICE_TEL).value
        context['office_mobile']=parameter_repo.parameter(name=ParameterEnum.OFFICE_MOBILE).value
        context['office_email']=parameter_repo.parameter(name=ParameterEnum.OFFICE_EMAIL).value
        return render(request,TEMPLATE_ROOT+"index.html",context)

class OurWorkViews(View):
    def ourwork(self,request,*args, **kwargs):
        context=getContext(request)
        context['body_class']="blog-post"
        context['main_class']='main-raised'
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        our_work=OurWorkRepo(request=request).our_work(*args, **kwargs)
        context.update(PageContext(request=request,page=our_work))
        context['our_work']=our_work
        return render(request,TEMPLATE_ROOT+"our-work.html",context)

class OurTeamViews(View):
    def ourteam(self,request,*args, **kwargs):
        context=getContext(request)
        context['body_class']="profile-page sidebar-collapse"
        context['main_class']='main-raised'
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        our_team=OurTeamRepo(request=request).our_team(*args, **kwargs)
        context.update(ProfileContext(request=request,profile=our_team.profile))
        context['our_team']=our_team
        return render(request,TEMPLATE_ROOT+"our-team.html",context)

class FeatureViews(View):
    def feature(self,request,*args, **kwargs):
        context=getContext(request)
        context['body_class']="blog-post"
        context['main_class']='main-raised'
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        feature=FeatureRepo(request=request).feature(*args, **kwargs)
        context.update(PageContext(request=request,page=feature))
        context['feature']=feature
        return render(request,TEMPLATE_ROOT+"feature.html",context)

class BlogViews(View):
    def blog(self,request,*args, **kwargs):
        context=getContext(request)
        context['body_class']="blog-post"
        context['main_class']='main-raised'
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        blog=BlogRepo(request=request).blog(*args, **kwargs)
        context.update(PageContext(request=request,page=blog))
        context['blog']=blog
        return render(request,TEMPLATE_ROOT+"blog.html",context)

    def blogs(self,request,*args, **kwargs):
        context=getContext(request)
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        blogs=BlogRepo(request=request).list(*args, **kwargs)
        context['blogs']=blogs
        return render(request,TEMPLATE_ROOT+"blogs.html",context)


class CryptoTokenViews(View):
    def crypto_token(self,request,*args, **kwargs):
        context=getContext(request)
        context['body_class']="blog-post"
        context['main_class']='main-raised'
        crypto_token=CryptoTokenRepo(request=request).crypto_token(*args, **kwargs)
        context.update(PageContext(request=request,page=crypto_token))
        context['crypto_token']=crypto_token
        return render(request,TEMPLATE_ROOT+"crypto-token.html",context)

    def crypto_tokens(self,request,*args, **kwargs):
        context=getContext(request)
        # parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        blogs=BlogRepo(request=request).list(*args, **kwargs)
        context['blogs']=blogs
        return render(request,TEMPLATE_ROOT+"blogs.html",context)


class ResumeViews(View):
    def resume_category(self,request,*args, **kwargs):
        context=getContext(request)
        resume_category=ResumeCategoryRepo(request=request).resume_category(*args, **kwargs)
        page=resume_category
        context.update(PageContext(request=request,page=page))
        return render(request,TEMPLATE_ROOT+"resume-category.html",context)

    def resume(self,request,*args, **kwargs):
        context=getContext(request)
        resume=ResumeRepo(request=request).resume(*args, **kwargs)
        page=resume
        context.update(PageContext(request=request,page=page))
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        return render(request,TEMPLATE_ROOT+"resume.html",context)
