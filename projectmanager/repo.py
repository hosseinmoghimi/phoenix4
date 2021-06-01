from django.db.models.query_utils import Q
from .apps import APP_NAME
from .models import Project,OrganizationUnit


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
            objects=objects.filter(Q(for_home=kwargs['for_home'])|Q(parent=None))
        return objects.all()
    def add_project(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_project"):
            return None
        new_project=Project()

        if 'title' in kwargs:
            new_project.title=kwargs['title']

        if 'parent_id' in kwargs:
            new_project.parent_id=kwargs['parent_id']
        
        new_project.save()
        return new_project



class OrganizationUnitRepo():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.objects=OrganizationUnit.objects
    def organization_unit(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'new_organization_id' in kwargs:
            return self.objects.filter(pk=kwargs['new_organization_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
    def get(self,*args, **kwargs):
        return self.organization_unit(*args, **kwargs)
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])        
        if 'for_home' in kwargs:
            objects=objects.filter(Q(for_home=kwargs['for_home'])|Q(parent=None))
        return objects.all()
    def add_organization_unit(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_organizationunit"):
            return None
        new_organization=OrganizationUnit()

        if 'title' in kwargs:
            new_organization.title=kwargs['title']

        if 'parent_id' in kwargs:
            new_organization.parent_id=kwargs['parent_id']
        
        new_organization.save()
        return new_organization