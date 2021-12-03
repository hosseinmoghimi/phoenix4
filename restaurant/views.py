from django.shortcuts import render
from django.views import View
from core.repo import ParameterRepo
from core.views import CoreContext
from restaurant.serializers import FoodSerializer, GuestSerializer, MealSerializer, ReservedMealSerializer,HostSerializer
from .forms import AddFoodForm, ReserveMealForm, ServeMealForm,AddHostForm
from .repo import FoodRepo, GuestRepo, MealRepo, ReservedMealRepo,HostRepo
from .apps import APP_NAME
import json


TEMPLATE_ROOT="restaurant/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
    me_guest=GuestRepo(request=request).me
    context['me_guest']=me_guest
    guests=[]
    if me_guest is not None:
        guests=[me_guest]
    context['guests_s']=json.dumps(GuestSerializer(guests,many=True).data)
    context['me_guest_s']=json.dumps(GuestSerializer(me_guest).data)
 
    return context


class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        guest=context['me_guest']
        if 'guest_id' in kwargs:
            guest=GuestRepo(request=request).guest(pk=kwargs['guest_id'])
        meals=MealRepo(request=request).list()
        context['meals']=meals

        

        meals=MealRepo(request=request).list(*args, **kwargs)
        if guest is not None:
            for meal in meals:
                meal.update_reserved(guest_id=guest.id)

        context['meals']=meals
        meals_s=json.dumps(MealSerializer(meals,many=True).data)
        context['meals_s']=meals_s


        foods=FoodRepo(request=request).list()
        context['foods']=foods
        context['foods_s']=json.dumps(FoodSerializer(foods,many=True).data)
        
        
        
        hosts=HostRepo(request=request).list()
        context['hosts']=hosts
        context['hosts_s']=json.dumps(HostSerializer(hosts,many=True).data)



        guests=GuestRepo(request=request).list()
        context['guests']=guests
        context['guests_s']=json.dumps(GuestSerializer(guests,many=True).data)

        
        context['reserve_meal_form']=ReserveMealForm()
        return render(request,TEMPLATE_ROOT+"index.html",context)


class GuestViews(View):
    def guest(self,request,*args, **kwargs):
        context=getContext(request=request)
        guest=GuestRepo(request=request).guest(*args, **kwargs)
        context['guest']=guest

        reserved_meals=ReservedMealRepo(request=request).list(guest_id=guest.id)
        context['reserved_meals']=reserved_meals
        reserved_meals_s=json.dumps(ReservedMealSerializer(reserved_meals,many=True).data)
        context['reserved_meals_s']=reserved_meals_s

        
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
        guest=GuestRepo(request=request).me
        context['guest']=guest
        reserved_meal_repo=ReservedMealRepo(request=request)
        reserved_meal=reserved_meal_repo.objects.filter(meal=meal).filter(guest=guest).first()
        context['reserved_meal']=reserved_meal
        if guest is not None and reserved_meal is None:
            context['reserve_meal_form']=ReserveMealForm()
        if request.user.has_perm(APP_NAME+".change_reservedmeal"):
            context['serve_meal_form']=ServeMealForm()
        if request.user.has_perm(APP_NAME+".view_reservedmeal"):
            served_meals=reserved_meal_repo.list(meal_id=meal.id).exclude(date_served=None).order_by('-date_served')
            served_meals_s=json.dumps(ReservedMealSerializer(served_meals,many=True).data)
            context['served_meals_s']=served_meals_s
        return render(request,TEMPLATE_ROOT+"meal.html",context)

    def reserved_meal(self,request,*args, **kwargs):
        context=getContext(request=request)
        reserved_meal=ReservedMealRepo(request=request).reserved_meal(*args, **kwargs)
        context['reserved_meal']=reserved_meal
        guest=GuestRepo(request=request).me
        context['guest']=guest
        return render(request,TEMPLATE_ROOT+"reserved-meal.html",context)

    def meals(self,request,*args, **kwargs):
        context=getContext(request=request)
        guest=GuestRepo(request=request).me
        meals=MealRepo(request=request).list(*args, **kwargs)
        context['meals']=meals
        guest=context['me_guest']
        if 'guest_id' in kwargs:
            guest=GuestRepo(request=request).guest(pk=kwargs['guest_id'])
        for meal in meals:
            meal.update_reserved(guest_id=guest.id)
        meals_s=json.dumps(MealSerializer(meals,many=True).data)
        context['meals_s']=meals_s
        guests=GuestRepo(request=request).list()
        context['guests_s']=json.dumps(GuestSerializer(guests,many=True).data)
        context['me_guest_s']=json.dumps(GuestSerializer(guest).data)
        context['me_guest']=guest
        context['reserve_meal_form']=ReserveMealForm()
        return render(request,TEMPLATE_ROOT+"meals.html",context)


class HostViews(View):
    def host(self,request,*args, **kwargs):
        context=getContext(request=request)
        host=HostRepo(request=request).host(*args, **kwargs)
        context['host']=host



        
        meals=MealRepo(request=request).list(host_id=host.id)
        context['meals']=meals
        meals_s=json.dumps(MealSerializer(meals,many=True).data)
        context['meals_s']=meals_s


        return render(request,TEMPLATE_ROOT+"host.html",context)
    def hosts(self,request,*args, **kwargs):
        context=getContext(request=request)
        hosts=HostRepo(request=request).list(*args, **kwargs)
        context['hosts']=hosts
        context['hosts_s']=json.dumps(HostSerializer(hosts,many=True).data)
        context['add_host_form']=AddHostForm()
        return render(request,TEMPLATE_ROOT+"hosts.html",context)


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