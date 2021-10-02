
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
                location=add_work_shift_form.cleaned_data['location']
                title=add_work_shift_form.cleaned_data['title']
                page_id=add_work_shift_form.cleaned_data['page_id']
                work_shift=WorkShiftRepo(request=request).add_work_shift(page_id=page_id,location=location,title=title)
                
                if work_shift is not None:
                    log=4
                    work_shift=WorkShiftSerializer(location).data
                    context['work_shift']=work_shift
                    context['result']=SUCCEED
        return JsonResponse(context)
    