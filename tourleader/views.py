import json
from django.shortcuts import render
from .forms import *
from chef.serializers import FoodSerializer
from .repo import FoodRepo
from .apps import APP_NAME
from core.views import CoreContext, PageContext
from django.views import View
TEMPLATE_ROOT="chef/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
# Create your views here.
class BasicView(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['chef_title']="CHEFFFFF TITLE"
        foods=FoodRepo(request=request).list(*args, **kwargs)
        if request.user.has_perm(APP_NAME+".add_food"):
            context['add_food_form']=AddFoodForm()
        context['foods']=foods
        context['foods_s']=json.dumps(FoodSerializer(foods,many=True).data)
        return render(request,TEMPLATE_ROOT+"index.html",context)

class FoodViews(View):
    def food(self,request,*args, **kwargs):
        context=getContext(request=request)
        food=FoodRepo(request=request).food(*args, **kwargs)
        context.update(PageContext(request=request,page=food))
        context['chef_title']="CHEFFFFF TITLE"
        context['food']=food
        return render(request,TEMPLATE_ROOT+"food.html",context)
    def foods(self,request,*args, **kwargs):
        context=getContext(request=request)
        foods=FoodRepo(request=request).list(*args, **kwargs)
        context['foods']=foods
        context['foods_s']=json.dumps(FoodSerializer(foods,many=True).data)
        if request.user.has_perm(APP_NAME+".add_food"):
            context['add_food_form']=AddFoodForm()
        return render(request,TEMPLATE_ROOT+"foods.html",context)