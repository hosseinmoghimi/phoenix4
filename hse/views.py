from django.shortcuts import render

# Create your views here.
from django.views import View
from core.enums import ParametersEnum

from core.repo import ParameterRepo
from .serializers import BlogSerializer
from .apps import APP_NAME
from django.shortcuts import render,reverse,redirect
from .repo import BlogRepo
from .forms import *
import json
from core.views import CoreContext,PageContext
TEMPLATE_ROOT="hse/"
layout_parent="phoenix/layout.html"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=layout_parent
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
 
    return context

class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        blogs=BlogRepo(request=request).list()
        context['blogs']=blogs
        blogs_s=json.dumps(BlogSerializer(blogs,many=True).data)
        context['blogs_s']=blogs_s
        add_blog_form=AddBlogForm()
        context['add_blog_form']=add_blog_form
        return render(request,TEMPLATE_ROOT+"index.html",context)
class BlogViews(View):
    def blog(self,request,*args, **kwargs):
        context=getContext(request=request)
        blog=BlogRepo(request=request).blog(*args, **kwargs)
        context.update(PageContext(request=request,page=blog))
        context['blog']=blog
        return render(request,TEMPLATE_ROOT+"blog.html",context)

