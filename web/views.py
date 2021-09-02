from . import constants
from core.repo import ParameterRepo
from django.shortcuts import render
from .repo import *
from django.views import View
from core.views import CoreContext, PageContext

# TEMPLATE_ROOT="material-dashboard-5/"
LAYOUT_PARENT='material-kit-pro/layout.html'
TEMPLATE_ROOT="web/"
# TEMPLATE_ROOT="my_resume_en/"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        context['body_class']="sections-page"        
        blogs=BlogRepo(request=request).list(for_home=True,*args, **kwargs)
        context['blogs']=blogs

        return render(request,TEMPLATE_ROOT+"index.html",context)

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

class OurworkViews(View):
    def ourwork(self,request,*args, **kwargs):
        context=getContext(request)
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        return render(request,TEMPLATE_ROOT+"index.html",context)

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
