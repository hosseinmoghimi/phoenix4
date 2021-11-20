from stock.models import Payment
from core.constants import FAILED,SUCCEED
from .serializers import FoodSerializer
from rest_framework.views import APIView
from .forms import AddFoodForm,ReserveMealForm
from .repo import FoodRepo, MealRepo
from django.http import JsonResponse


class FoodApi(APIView):
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
                 
                meal=MealRepo(request=request).reserve_meal(
                    meal_id=meal_id,
                    guest_id=guest_id,
                    )

                if meal is not None:
                    context['meal']=MealSerializer(meal).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
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