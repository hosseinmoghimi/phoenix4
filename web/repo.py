from ast import keyword
from khayyam import constants
from django.db.models import Q
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
        self.objects = Blog.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for) | Q(meta_data__contains=search_for)|Q(description__contains=search_for))
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




class CryptoTokenRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = CryptoToken.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for) | Q(meta_data__contains=search_for)|Q(description__contains=search_for))
        return objects
    def crypto_token(self,*args, **kwargs):
        pk=0
        if 'crypto_token_id' in kwargs:
            pk=kwargs['crypto_token_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_crypto_token(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_blog"):
            return
        
        crypto_token=CryptoToken()
        if 'title' in kwargs:
            crypto_token.title=kwargs['title']
        if 'for_home' in kwargs:
            crypto_token.for_home=kwargs['for_home']
        
        crypto_token.save()
        return crypto_token


class OurTeamRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = OurTeam.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects
    def our_team(self,*args, **kwargs):
        pk=0
        if 'our_team_id' in kwargs:
            pk=kwargs['our_team_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
   
   


class TestimonialRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Testimonial.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects
    def testimonial(self,*args, **kwargs):
        pk=0
        if 'testimonial_id' in kwargs:
            pk=kwargs['testimonial_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
   
   
class FeatureRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Feature.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects
    def feature(self,*args, **kwargs):
        pk=0
        if 'feature_id' in kwargs:
            pk=kwargs['feature_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
   
   

class OurWorkRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = OurWork.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects
    def our_work(self,*args, **kwargs):
        pk=0
        if 'our_work_id' in kwargs:
            pk=kwargs['our_work_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_our_work(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_ourwork"):
            return
        
        our_work=OurWork()
        if 'title' in kwargs:
            our_work.title=kwargs['title']
        if 'for_home' in kwargs:
            our_work.for_home=kwargs['for_home']
        
        our_work.save()
        return our_work


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
        self.objects = Carousel.objects.order_by('priority')
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