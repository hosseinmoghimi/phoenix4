from core import repo as CoreRepo
from .models import Location

class LocationRepo():
    def __init__(self,user):
        self.objects=Location.objects
        self.user=user
        self.profile=CoreRepo.ProfileRepo(user).me
    def list(self,*args, **kwargs):
        return self.objects.all()
    def location(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None

