from django.db.models.aggregates import Avg
from django.utils import timezone
from .enums import BlogStatusEnum
from authentication.repo import ProfileRepo
from django.db.models import Q,Sum
from .apps import APP_NAME
from .models import Blog
from core.repo import ParameterRepo
from .enums import ParametersEnum

def show_archives(request):
        parameter_repo = ParameterRepo(request=request,app_name=APP_NAME)
        show_archives=parameter_repo.parameter(ParametersEnum.SHOW_ARCHIVES).boolean_value
        return show_archives
class BlogRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=Blog.objects.all()
        
        if_show_archives=show_archives(request=self.request)
        self.objects=self.objects.all()
        if not if_show_archives:
            self.objects=self.objects.filter(archive=False)
          

    def blog(self, *args, **kwargs):
        
        if 'blog_id' in kwargs:
            pk=kwargs['blog_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_blog(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_blog"):
            return 

        blog=Blog()

        if 'title' in kwargs:
            blog.title=kwargs['title']

        if 'description' in kwargs:
            blog.description=kwargs['description']

        if 'year' in kwargs:
            blog.year=kwargs['year']


        if 'amount' in kwargs:
            blog.amount=kwargs['amount']
        blog.save()
        return blog
