from core.constants import SUCCEED
from realestate.forms import AddPropertyFeatureForm, AddPropertyLocationForm
from rest_framework.views import APIView
from .serializers import PropertyFeatureSerializer
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
    def add_feature(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method == 'POST':
            log=2
            add_feature_form=AddPropertyFeatureForm(request.POST)
            if add_feature_form.is_valid():
                log=3
                property_id=add_feature_form.cleaned_data['property_id']
                name=add_feature_form.cleaned_data['name']
                value=add_feature_form.cleaned_data['value']
                property_feature=PropertyRepo(request=request).add_feature(property_id=property_id,name=name,value=value)
                if property_feature is not None:
                    context['property_feature']=PropertyFeatureSerializer(property_feature).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)