from .apps import APP_NAME
from authentication.repo import ProfileRepo
from .models import Property,PropertyMedia
from django.db.models import Q



class PropertyRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Property.objects
        self.me=ProfileRepo(user=self.user).me
    def property(self, *args, **kwargs):
        pk=0
        if 'property_id' in kwargs:
            pk=kwargs['property_id']
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
        return objects.all()
    def add_location(self,*args, **kwargs):
        if self.user.has_perm(APP_NAME+".change_property"):
            property=self.property(*args, **kwargs)
            if property is not None and 'location' in kwargs:
                location=kwargs['location']
                property.location=location
                print(property)
                print(property.location)
                property.save()
                return location
