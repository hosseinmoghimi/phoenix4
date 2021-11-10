from .models import Appointment
from authentication.repo import ProfileRepo
class AppointmentRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        if self.profile is not None:
            self.objects=Appointment.objects.filter(creator=self.profile)
        else:
            self.objects=Appointment.objects.filter(pk=0)

  

    def add_appointment(self, *args, **kwargs):        
        pass
    def appointment(self, *args, **kwargs):        
        if 'appointment_id' in kwargs:
            pk=kwargs['appointment_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.appointment(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        return objects.all()
