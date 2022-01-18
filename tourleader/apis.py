from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from .repo import FoodRepo
from django.http import JsonResponse
from .forms import *
from .serializers import FoodSerializer
class FoodApi(APIView):
    def add_food(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            add_food_form=AddFoodForm(request.POST)
            if add_food_form.is_valid():
                fm=add_food_form.cleaned_data
                title=fm['title']
                food=FoodRepo(request=request).add_food(title=title)
                if food is not None:
                    context['food']=FoodSerializer(food).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
