from django.shortcuts import render
from django.views import View
from core.repo import ParameterRepo
from core.views import CoreContext
from restaurant.serializers import FoodSerializer, GuestSerializer, MealSerializer
from .forms import AddFoodForm
from .repo import FoodRepo, GuestRepo, MealRepo
from .apps import APP_NAME
import json


TEMPLATE_ROOT="restaurant/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
    context['app']={
        'home_url':parameter_repo.parameter(name='آدرس خانه').value,
        'title':parameter_repo.parameter(name='عنوان').value,
    }
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)


        meals=MealRepo(request=request).list()
        context['meals']=meals

        

        meals=MealRepo(request=request).list(*args, **kwargs)
        context['meals']=meals
        meals_s=json.dumps(MealSerializer(meals,many=True).data)
        context['meals_s']=meals_s


        foods=FoodRepo(request=request).list()
        context['foods']=foods
        context['foods_s']=json.dumps(FoodSerializer(foods,many=True).data)



        guests=GuestRepo(request=request).list()
        context['guests']=guests

        
        return render(request,TEMPLATE_ROOT+"index.html",context)

class GuestViews(View):
    def guest(self,request,*args, **kwargs):
        context=getContext(request=request)
        guest=GuestRepo(request=request).guest(*args, **kwargs)
        context['guest']=guest
        return render(request,TEMPLATE_ROOT+"guest.html",context)

    def guests(self,request,*args, **kwargs):
        context=getContext(request=request)
        guests=GuestRepo(request=request).list(*args, **kwargs)
        context['guests']=guests
        context['guests_s']=json.dumps(GuestSerializer(guests,many=True).data)
        return render(request,TEMPLATE_ROOT+"guests.html",context)


class MealViews(View):
    def meal(self,request,*args, **kwargs):
        context=getContext(request=request)
        meal=MealRepo(request=request).meal(*args, **kwargs)
        context['meal']=meal
        return render(request,TEMPLATE_ROOT+"meal.html",context)

    def meals(self,request,*args, **kwargs):
        context=getContext(request=request)
        meals=MealRepo(request=request).list(*args, **kwargs)
        context['meals']=meals
        meals_s=json.dumps(MealSerializer(meals,many=True).data)
        context['meals_s']=meals_s
        return render(request,TEMPLATE_ROOT+"meals.html",context)


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