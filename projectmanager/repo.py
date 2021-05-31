from .apps import APP_NAME
TEMPLATE_ROOT=APP_NAME+"/"
from .models import Project


class ProjectRepo():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.objects=Project.objects
    def project(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'project_id' in kwargs:
            return self.objects.filter(pk=kwargs['project_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
    def get(self,*args, **kwargs):
        return self.project(*args, **kwargs)
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])        
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects.all()