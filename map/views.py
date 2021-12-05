from django.shortcuts import render,reverse
import json
from core.enums import ParametersEnum

from core.repo import ParameterRepo
from map.forms import AddLocationForm
from .repo import *
from .serializers import *
from django.http import Http404
from django.views import View
from core.views import CoreContext, MessageView
from .apps import APP_NAME
TEMPLATE_ROOT = APP_NAME+"/"
layout_parent = "phoenix/layout.html"


def getContext(request):
    user = request.user
    context = CoreContext(request=request, app_name=APP_NAME)
    parameter_repo = ParameterRepo(app_name=APP_NAME)
 
     
    context['layout_parent'] = layout_parent
    return context


class BasicViews(View):
    def location(self, request, pk, *args, **kwargs):
        context = getContext(request)
        location = LocationRepo(request=request).location(pk)
        context['location'] = location
        context['location_s'] = json.dumps(LocationSerializer(location).data)

        return render(request, TEMPLATE_ROOT+"location.html", context)

class BasicViews(View):
    def home(self, request, *args, **kwargs):
        context = getContext(request)
        locations = LocationRepo(request=request).list(*args, **kwargs)
        context['locations'] = locations
        context['locations_s'] = json.dumps(LocationSerializer(locations,many=True).data)
        return render(request, TEMPLATE_ROOT+"index.html", context)


class LocationViews(View):
    def location(self, request, *args, **kwargs):
        context = getContext(request)
        location = LocationRepo(request=request).location(*args, **kwargs)
        context['location'] = location
        context['location_s'] = json.dumps(LocationSerializer(location).data)

        return render(request, TEMPLATE_ROOT+"location.html", context)
    def locations(self, request, *args, **kwargs):
        context = getContext(request)
        locations = LocationRepo(request=request).list(*args, **kwargs)
        context['locations'] = locations
        context['locations_s'] = json.dumps(LocationSerializer(locations,many=True).data)
        if request.user.has_perm(APP_NAME+".add_location"):
            context['add_location_form']=AddLocationForm()
        return render(request, TEMPLATE_ROOT+"locations.html", context)