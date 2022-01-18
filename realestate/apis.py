from core.constants import FAILED, SUCCEED
from core.serializers import ImageSerializer
from realestate.forms import AddPropertyFeatureForm, AddPropertyImageForm, AddPropertyLocationForm
from rest_framework.views import APIView
from .serializers import PropertyFeatureSerializer
from django.http import JsonResponse
from .repo import PropertyRepo

class PropertyApi(APIView):
    def add_property_image(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_image_form = AddPropertyImageForm(request.POST, request.FILES)
            if add_page_image_form.is_valid():
                log += 1
                title = add_page_image_form.cleaned_data['title']
                property_id = add_page_image_form.cleaned_data['property_id']
                image = request.FILES['image']
                image = PropertyRepo(request=request).add_image(
                    title=title, image=image, property_id=property_id)
                if image is not None:
                    context['image'] = ImageSerializer(
                        image, context={'request': request}).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

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