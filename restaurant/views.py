from django.shortcuts import render
from django.views import View
from core.views import CoreContext
from restaurant.serializers import FoodSerializer
from .forms import AddFoodForm
from .repo import FoodRepo, GuestRepo, MealRepo
from .apps import APP_NAME
import json


TEMPLATE_ROOT="restaurant/"
LAYOUT_PARENT="phoenix/layout.html"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)


        meals=MealRepo(request=request).list()
        context['meals']=meals

        


        foods=FoodRepo(request=request).list()
        context['foods']=foods
        context['foods_s']=json.dumps(FoodSerializer(foods,many=True).data)



        guests=GuestRepo(request=request).list()
        context['guests']=guests

        
        return render(request,TEMPLATE_ROOT+"index.html",context)


class FoodViews(View):
    def food(self,request,*args, **kwargs):
        context=getContext(request=request)
        food=FoodRepo(request=request).food(*args, **kwargs)
        context['food']=food
        return render(request,TEMPLATE_ROOT+"food.html",context)
    def foods(self,request,*args, **kwargs):
        context=getContext(request=request)
        foods=FoodRepo(request=request).list(*args, **kwargs)
        context['foods']=foods
        context['foods_s']=json.dumps(FoodSerializer(foods,many=True).data)
        context['add_food_form']=AddFoodForm()
        return render(request,TEMPLATE_ROOT+"foods.html",context)