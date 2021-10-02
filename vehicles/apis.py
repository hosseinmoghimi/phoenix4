
from utility.persian import PersianCalendar
from core.constants import SUCCEED,FAILED
from rest_framework.views import APIView
from django.http import JsonResponse

from vehicles.repo import WorkShiftRepo
from vehicles.serializers import WorkShiftSerializer
from .forms import *


class WorkShiftApi(APIView):
    def add_work_shift(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_work_shift_form=AddWorkShiftForm(request.POST)
            if add_work_shift_form.is_valid():
                log=3
                
                driver_id=add_work_shift_form.cleaned_data['driver_id']
                vehicle_id=add_work_shift_form.cleaned_data['vehicle_id']
                start_datetime=add_work_shift_form.cleaned_data['start_datetime']
                end_datetime=add_work_shift_form.cleaned_data['end_datetime']
                area_id=add_work_shift_form.cleaned_data['area_id']
                description=add_work_shift_form.cleaned_data['description']
                income=add_work_shift_form.cleaned_data['income']
                outcome=add_work_shift_form.cleaned_data['outcome']
                end_datetime=PersianCalendar().to_gregorian(end_datetime)
                start_datetime=PersianCalendar().to_gregorian(start_datetime)
                work_shift=WorkShiftRepo(request=request).add_work_shift(
                    area_id=area_id,
                    income=income,
                    outcome=outcome,
                    description=description,
                    driver_id=driver_id,
                    vehicle_id=vehicle_id,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime)
                
                if work_shift is not None:
                    log=4
                    work_shift=WorkShiftSerializer(work_shift).data
                    context['work_shift']=work_shift
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    