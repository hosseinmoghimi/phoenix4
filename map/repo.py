from authentication.repo import ProfileRepo
from core import repo as CoreRepo
from .apps import APP_NAME
from .models import Location

class LocationRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects = Location.objects
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        return objects
    def location(self,*args, **kwargs):
        
        if 'location_id' in kwargs:
            pk=kwargs['location_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_location"):
            return None
        location1=""
        title=""
        if 'location' in kwargs:
            location1=kwargs['location']
        if 'title' in kwargs:
            title=kwargs['title']
        location=Location()
        location.title=title
        location.creator=self.profile
        location.location=location1
        location.latitude="gfgf"
        location.longitude="gfgf"
        location.save()
        return location
