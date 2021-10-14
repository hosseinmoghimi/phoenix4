from .apps import APP_NAME
from rest_framework.views import APIView
from .repo import AppointmentRepo
from .forms import *

class LocationApi(APIView):
    def add_location(self,request):
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_location_form=AddLocationForm(request.POST)
            if add_location_form.is_valid():
                log=3
                location=add_location_form.cleaned_data['location']
                title=add_location_form.cleaned_data['title']
                page_id=add_location_form.cleaned_data['page_id']
                location=LocationRepo(request=request).add_location(page_id=page_id,location=location,title=title)
                
                if location is not None:
                    log=4
                    location_s=LocationSerializer(location).data
                    return JsonResponse({'result':SUCCEED,'location':location_s})
        return JsonResponse({'result':FAILED,'log':log})
    