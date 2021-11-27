from .models import ResumeCategory,Resume
from authentication.repo import ProfileRepo

class ResumeRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=Resume.objects
    def resume(self, *args, **kwargs):
        pk=0
        if 'resume_id' in kwargs:
            return self.objects.filter(pk=kwargs['resume_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

   
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'category_id' in kwargs:
            objects = objects.filter(category_id=kwargs['category_id'])
        
        return objects

    def category_list(self, *args, **kwargs):
        objects = ResumeCategory.objects.all()
        if 'profile_id' in kwargs:
            objects = objects.filter(profile_id=kwargs['profile_id'])
        
        return objects

