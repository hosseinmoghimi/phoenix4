from rest_framework.views import APIView
from .serializers import *
from .repo import *
from django.http import JsonResponse
from .forms import *
from utility.persian import PersianCalendar
from core.constants import SUCCEED,FAILED

class BasicApi(APIView):
    def enter_animal_to_saloon(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            enter_animal_to_saloon_form=EnterAnimalToSaloonForm(request.POST)
            if enter_animal_to_saloon_form.is_valid():
                log=3
                animal_tag=enter_animal_to_saloon_form.cleaned_data['animal_tag']
                saloon_id=enter_animal_to_saloon_form.cleaned_data['saloon_id']
                enter_date=enter_animal_to_saloon_form.cleaned_data['enter_date']
                animal_price=enter_animal_to_saloon_form.cleaned_data['animal_price']
                animal_weight=enter_animal_to_saloon_form.cleaned_data['animal_weight']
               
                enter_date=PersianCalendar().to_gregorian(enter_date)
                res=SaloonRepo(request.user).enter_animal_to_saloon(animal_price=animal_price,animal_weight=animal_weight,animal_tag=animal_tag,saloon_id=saloon_id,enter_date=enter_date)
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


    def saloon_daily_report(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            saloon_daily_report_form=SaloonDailyReportForm(request.POST)
            if saloon_daily_report_form.is_valid():
                log=3
                saloon_id=saloon_daily_report_form.cleaned_data['saloon_id']
                report_date=saloon_daily_report_form.cleaned_data['report_date']
                context['report_date']=report_date
                report_date=PersianCalendar().to_gregorian(report_date)
                animals_in_saloon=SaloonRepo(request.user).animals_in_saloon(saloon_id=saloon_id,report_date=report_date)
                animals_in_saloon_s=AnimalInSaloonSerializer(animals_in_saloon,many=True).data
                
                context['animals_in_saloon']=animals_in_saloon_s
                saloon_foods=SaloonRepo(request.user).saloon_foods(saloon_id=saloon_id,report_date=report_date)
                saloon_foods_s=SaloonFoodSerializer(saloon_foods,many=True).data
                context['saloon_foods']=saloon_foods_s
                context['result']=SUCCEED
                        
                
        context['log']=log
        return JsonResponse(context)

