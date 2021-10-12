from django.http.response import JsonResponse
from core.constants import FAILED,SUCCEED
from salary.forms import AddEmployeeSalaryForm
from salary.models import EmployeeSalary
from salary.repo import EmployeeSalaryRepo
from salary.serializers import EmployeeSalarySerializer
from .apps import APP_NAME
from rest_framework.views import APIView

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