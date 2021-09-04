from khayyam import constants
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
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects
    def blog(self,*args, **kwargs):
        pk=0
        if 'blog_id' in kwargs:
            pk=kwargs['blog_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_blog(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_blog"):
            return
        
        blog=Blog()
        if 'title' in kwargs:
            blog.title=kwargs['title']
        if 'for_home' in kwargs:
            blog.for_home=kwargs['for_home']
        
        blog.save()
        return blog



class CarouselRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.app_name=""
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']
        self.objects = Carousel.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']
        return self.objects.filter(app_name=self.app_name)
    
class ContactMessageRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.app_name=""
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']
        self.objects = ContactMessage.objects
        self.me=ProfileRepo(user=self.user).me
    def add(self,*args, **kwargs):
        contact_message=ContactMessage()
        contact_message.app_name=self.app_name
        if 'full_name' in kwargs:
            contact_message.full_name=kwargs['full_name']
        if 'subject' in kwargs:
            contact_message.subject=kwargs['subject']
        if 'email' in kwargs:
            contact_message.email=kwargs['email']
        if 'message' in kwargs:
            contact_message.message=kwargs['message']
        if 'mobile' in kwargs:
            contact_message.mobile=kwargs['mobile']
        contact_message.save()
        return contact_message