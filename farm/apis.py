from rest_framework.views import APIView
from .serializers import *
from .repo import *
from django.http import JsonResponse
from .forms import *
from utility.persian import PersianCalendar
from core.constants import SUCCEED,FAILED

class BasicApi(APIView):
    def do_koshtar(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            do_koshtar_form=DoKoshtarForm(request.POST)
            if do_koshtar_form.is_valid():
                log=3
                tag=do_koshtar_form.cleaned_data['tag']
                koshtar_date=do_koshtar_form.cleaned_data['koshtar_date']
                # price=forms.IntegerField(required=False)
                weight=do_koshtar_form.cleaned_data['weight']
                Jegar_price=do_koshtar_form.cleaned_data['Jegar_price']
                Kalle_pache_price=do_koshtar_form.cleaned_data['Kalle_pache_price']
                pust_price=do_koshtar_form.cleaned_data['pust_price']
                transport_fee=do_koshtar_form.cleaned_data['transport_fee']
                koshtar_fee=do_koshtar_form.cleaned_data['koshtar_fee']
                lashe_price=do_koshtar_form.cleaned_data['lashe_price']
                lashe_weight=do_koshtar_form.cleaned_data['lashe_weight']
                description = do_koshtar_form.cleaned_data['description']

               

                koshtar_date=PersianCalendar().to_gregorian(koshtar_date)
                koshtar=KoshtarRepo(request=request).do_koshtar(
                    tag=tag,
                    koshtar_date=koshtar_date,
                    weight=weight,
                    Jegar_price=Jegar_price,
                    Kalle_pache_price=Kalle_pache_price,
                    pust_price=pust_price,
                    transport_fee=transport_fee,
                    koshtar_fee=koshtar_fee,
                    lashe_price=lashe_price,
                    lashe_weight=lashe_weight,
                    description=description,
                    )
                if koshtar is not None:
                    context['koshtar']=KoshtarSerializer(koshtar).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def add_cost(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            add_cost_form=AddCostForm(request.POST)
            if add_cost_form.is_valid():
                log=3
                value=add_cost_form.cleaned_data['value']
                saloon_id=add_cost_form.cleaned_data['saloon_id']
                cost_date=add_cost_form.cleaned_data['cost_date']
                category=add_cost_form.cleaned_data['category']
                employee_id=add_cost_form.cleaned_data['employee_id']
               
                cost_date=PersianCalendar().to_gregorian(cost_date)
                cost=CostRepo(request=request).add_cost(
                    value=value,
                    employee_id=employee_id,
                    saloon_id=saloon_id,
                    category=category,
                    cost_date=cost_date)
                if cost is not None:
                    context['cost']=CostSerializer(cost).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def enter_animal_to_saloon(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            enter_animal_to_saloon_form=EnterAnimalToSaloonForm(request.POST)
            if enter_animal_to_saloon_form.is_valid():
                log=3
                animal_id=enter_animal_to_saloon_form.cleaned_data['animal_id']
                saloon_id=enter_animal_to_saloon_form.cleaned_data['saloon_id']
                enter_date=enter_animal_to_saloon_form.cleaned_data['enter_date']
                animal_price=enter_animal_to_saloon_form.cleaned_data['animal_price']
                animal_weight=enter_animal_to_saloon_form.cleaned_data['animal_weight']
               
                enter_date=PersianCalendar().to_gregorian(enter_date)
                animal_in_saloon=SaloonRepo(request=request).enter_animal_to_saloon(animal_price=animal_price,animal_weight=animal_weight,saloon_id=saloon_id,animal_id=animal_id,enter_date=enter_date)
                if animal_in_saloon is not None:
                    context['animal_in_saloon']=AnimalInSaloonSerializer(animal_in_saloon).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def add_animal(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            add_new_animal_form=AddNewAnimalForm(request.POST)
            if add_new_animal_form.is_valid():
                log=3
                category=add_new_animal_form.cleaned_data['category']
                tag=add_new_animal_form.cleaned_data['tag']
                saloon_id=add_new_animal_form.cleaned_data['saloon_id']
                enter_date=add_new_animal_form.cleaned_data['enter_date']
                price=add_new_animal_form.cleaned_data['price']
                weight=add_new_animal_form.cleaned_data['weight']
               
                enter_date=PersianCalendar().to_gregorian(enter_date)
                animal_in_saloon=AnimalRepo(request=request).add_new_animal(category=category,price=price,weight=weight,tag=tag,saloon_id=saloon_id,enter_date=enter_date)
                if animal_in_saloon is not None:
                    context['animal_in_saloon']=AnimalInSaloonSerializer(animal_in_saloon).data
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
                animals_in_saloon=SaloonRepo(request=request).animals_in_saloon(saloon_id=saloon_id,report_date=report_date)
                animals_in_saloon_s=AnimalInSaloonSerializer(animals_in_saloon,many=True).data
                
                context['animals_in_saloon']=animals_in_saloon_s
                saloon_foods=SaloonRepo(request=request).saloon_foods(saloon_id=saloon_id,report_date=report_date)
                saloon_foods_s=SaloonFoodSerializer(saloon_foods,many=True).data
                context['saloon_foods']=saloon_foods_s
                context['result']=SUCCEED
                        
                
        context['log']=log
        return JsonResponse(context)

