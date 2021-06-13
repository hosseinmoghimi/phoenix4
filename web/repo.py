from authentication.repo import ProfileRepo
from .models import *

class ResumeCategoryRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = ResumeCategory.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        return self.objects.all()
    def resume_category(self,*args, **kwargs):
        if 'resume_category_id' in kwargs:
            pk=kwargs['resume_category_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
class ResumeRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Resume.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        return self.objects.all()
    def resume_category(self,*args, **kwargs):
        if 'resume_id' in kwargs:
            pk=kwargs['resume_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()



class BlogRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Blog.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        return self.objects.all()
    def resume_category(self,*args, **kwargs):
        if 'blog_id' in kwargs:
            pk=kwargs['blog_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()


