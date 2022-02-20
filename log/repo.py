from .models import Log
from authentication.repo import ProfileRepo
from .apps import APP_NAME

class LogRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Log.objects.order_by('-date_added')
        self.profile = ProfileRepo(user=self.user).me

        if self.user.has_perm(APP_NAME+".view_log"):
            self.objects = self.objects
        else:
            self.objects = self.objects.filter(pk__lte=0)


    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def log(self, *args, **kwargs):
        if 'log_id' in kwargs:
            return self.objects.filter(pk= kwargs['log_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()    
        
    def add_log(self,*args, **kwargs):
        log=Log()
        if 'title' in kwargs:            
            log.title=kwargs['title']
        if 'app_name' in kwargs:     
            log.app_name=kwargs['app_name']
        if 'description' in kwargs:            
            log.description=kwargs['description']
        log.save()
        return log