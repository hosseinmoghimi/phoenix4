from stock.models import Payment
from core.constants import FAILED,SUCCEED
from .serializers import FoodSerializer, MealSerializer, ReservedMealSerializer
from rest_framework.views import APIView
from .forms import AddFoodForm,ReserveMealForm, ServeMealForm, UnreserveMealForm
from .repo import FoodRepo, MealRepo, ReservedMealRepo
from django.http import JsonResponse
 
class MealApi(APIView):
    def reserve_meal(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            reserve_meal_form=ReserveMealForm(request.POST)
            if reserve_meal_form.is_valid():
                log+=1
                meal_id=reserve_meal_form.cleaned_data['meal_id']
                guest_id=reserve_meal_form.cleaned_data['guest_id']
                quantity=reserve_meal_form.cleaned_data['quantity']
                 
                reserved_meal=ReservedMealRepo(request=request).reserve_meal(
                    meal_id=meal_id,
                    guest_id=guest_id,
                    quantity=quantity
                    )

                if reserved_meal is not None:
                    context['reserved_meal']=ReservedMealSerializer(reserved_meal).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def unreserve_meal(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=100
        if request.method=='POST':
            log=200
            unreserve_meal_form=UnreserveMealForm(request.POST)
            if unreserve_meal_form.is_valid():
                log=300
                meal_id=unreserve_meal_form.cleaned_data['meal_id']
                guest_id=unreserve_meal_form.cleaned_data['guest_id']
                 
                meal=ReservedMealRepo(request=request).unreserve_meal(
                    meal_id=meal_id,
                    guest_id=guest_id,
                    )

                if meal is not None:
                    context['meal']=MealSerializer(meal).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def serve_meal(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            serve_meal_form=ServeMealForm(request.POST)
            if serve_meal_form.is_valid():
                log+=1
                meal_id=serve_meal_form.cleaned_data['meal_id']
                guest_id=serve_meal_form.cleaned_data['guest_id']
                 
                served_meal=ReservedMealRepo(request=request).serve_meal(
                    meal_id=meal_id,
                    guest_id=guest_id,
                    )


                if served_meal is not None:
                    context['served_meal']=ReservedMealSerializer(served_meal).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def unserve_meal(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            serve_meal_form=ServeMealForm(request.POST)
            if serve_meal_form.is_valid():
                log+=1
                meal_id=serve_meal_form.cleaned_data['meal_id']
                guest_id=serve_meal_form.cleaned_data['guest_id']
                 
                reserved_meal=ReservedMealRepo(request=request).unserve_meal(
                    meal_id=meal_id,
                    guest_id=guest_id,
                    )


                if reserved_meal is not None:
                    context['reserved_meal']=ReservedMealSerializer(reserved_meal).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class FoodApi(APIView):
    def add_food(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_food_form=AddFoodForm(request.POST)
            if add_food_form.is_valid():
                log+=1
                title=add_food_form.cleaned_data['title']
                 
                food=FoodRepo(request=request).add_food(
                    title=title,
                    )

                if food is not None:
                    context['food']=FoodSerializer(food).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)