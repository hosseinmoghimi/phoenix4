from django.http.response import JsonResponse
from core.constants import FAILED,SUCCEED
from salary.enums import SalaryDirectionEnum
from salary.forms import AddEmployeeSalaryForm, AddSalaryLineForm, AddVacationForm
from salary.models import EmployeeSalary
from salary.repo import EmployeeSalaryRepo, SalaryLineRepo, VacationRepo
from salary.serializers import EmployeeSalarySerializer, SalaryLineSerializer, VacationSerializer
from .apps import APP_NAME
from rest_framework.views import APIView

class VacationApi(APIView):
    def add_vacation(selff,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            add_vacation_form=AddVacationForm(request.POST)
            if add_vacation_form.is_valid():
                log=3
                employee_id=add_vacation_form.cleaned_data['employee_id']
                title=add_vacation_form.cleaned_data['title']
                vacation=VacationRepo(request=request).add_vacation(
                    employee_id=employee_id,
                    title=title,
                )
                if vacation is not None:
                    context['vacation']=VacationSerializer(vacation).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class EmployeeSalaryApi(APIView):
    def add_employee_salary(selff,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            add_employee_salary_form=AddEmployeeSalaryForm(request.POST)
            if add_employee_salary_form.is_valid():
                log=3
                employee_id=add_employee_salary_form.cleaned_data['employee_id']
                year=add_employee_salary_form.cleaned_data['year']
                month=add_employee_salary_form.cleaned_data['month']
                month_name=add_employee_salary_form.cleaned_data['month_name']
                employee_salary=EmployeeSalaryRepo(request=request).add_employee_salary(
                    employee_id=employee_id,
                    year=year,
                    month=month,
                    month_name=month_name,
                )
                if employee_salary is not None:
                    context['employee_salary']=EmployeeSalarySerializer(employee_salary).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


    def add_salary_line(selff,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            add_salary_line_form=AddSalaryLineForm(request.POST)
            if add_salary_line_form.is_valid():
                log=3
                employee_salary_id=add_salary_line_form.cleaned_data['employee_salary_id']
                direction=add_salary_line_form.cleaned_data['direction']
                title=add_salary_line_form.cleaned_data['title']
                amount=add_salary_line_form.cleaned_data['amount']
                description=add_salary_line_form.cleaned_data['description']
                
                direction=SalaryDirectionEnum.MAZAYA if direction==1 else SalaryDirectionEnum.KOSURAT
                
                salary_line=SalaryLineRepo(request=request).add_salary_line(
                    employee_salary_id=employee_salary_id,
                    direction=direction,
                    amount=amount,
                    title=title,
                    description=description,
                )
                if salary_line is not None:
                    if salary_line.direction==SalaryDirectionEnum.MAZAYA:
                        context['positive_line']=SalaryLineSerializer(salary_line).data
                    if salary_line.direction==SalaryDirectionEnum.KOSURAT:
                        context['negative_line']=SalaryLineSerializer(salary_line).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)