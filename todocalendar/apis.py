from authentication.serializers import ProfileSerializer
from .apps import APP_NAME
from rest_framework.views import APIView
from .repo import AppointmentRepo
from .forms import AddAppointmentForm, AddPersonForm
from django.http import JsonResponse
from .serializers import AppointmentSerializer
from core.constants import FAILED,SUCCEED

class AppointmentApi(APIView):
    def add_location(self,request):
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_appointment_form=AddAppointmentForm(request.POST)
            if add_appointment_form.is_valid():
                log=3
                location=add_appointment_form.cleaned_data['location']
                title=add_appointment_form.cleaned_data['title']
                page_id=add_appointment_form.cleaned_data['page_id']
                appointment=AppointmentRepo(request=request).add_appointment(page_id=page_id,location=location,title=title)
                
                if appointment is not None:
                    log=4
                    appointment_s=AppointmentSerializer(appointment).data
                    return JsonResponse({'result':SUCCEED,'appointment':appointment_s})
        return JsonResponse({'result':FAILED,'log':log})
    
    def add_person(self,request):
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_appointment_form=AddPersonForm(request.POST)
            if add_appointment_form.is_valid():
                log=3
                profile_id=add_appointment_form.cleaned_data['profile_id']
                appointment_id=add_appointment_form.cleaned_data['appointment_id']
                person=AppointmentRepo(request=request).add_person(appointment_id=appointment_id,profile_id=profile_id)
                
                if person is not None:
                    log=4
                    person=ProfileSerializer(person).data
                    return JsonResponse({'result':SUCCEED,'person':person})
        return JsonResponse({'result':FAILED,'log':log})
    