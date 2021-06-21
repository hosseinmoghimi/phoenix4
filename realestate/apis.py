from core.constants import SUCCEED
from realestate.forms import AddPropertyLocationForm
from rest_framework.views import APIView

from django.http import JsonResponse
from .repo import PropertyRepo

class PropertyApi(APIView):
    def add_location(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method == 'POST':
            log=2
            add_location_form=AddPropertyLocationForm(request.POST)
            if add_location_form.is_valid():
                log=3
                property_id=add_location_form.cleaned_data['property_id']
                location=add_location_form.cleaned_data['location']
                location=PropertyRepo(request=request).add_location(property_id=property_id,location=location)
                if location is not None:
                    context['location']=location
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)