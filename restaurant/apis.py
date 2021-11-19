from stock.models import Payment
from core.constants import FAILED,SUCCEED
from .serializers import FoodSerializer
from rest_framework.views import APIView
from .forms import AddFoodForm
from .repo import FoodRepo
from django.http import JsonResponse
from utility.persian import PersianCalendar


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