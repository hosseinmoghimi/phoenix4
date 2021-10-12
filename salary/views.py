from django.shortcuts import render,reverse
from django.http import Http404
from salary.forms import AddEmployeeSalaryForm
from salary.repo import EmployeeSalaryRepo
from .apps import APP_NAME
from django.views import View
from projectmanager.repo import EmployeeRepo
from core.views import  PageContext,CoreContext
from core.repo import ParameterRepo,PictureRepo,ParametersEnum
from utility.persian import PERSIAN_MONTH_NAMES
TEMPLATE_ROOT="salary/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
    context['app'] = {
        'home_url': reverse(APP_NAME+":home"),
        'tel': parameter_repo.get(ParametersEnum.TEL).value,
        'title': parameter_repo.get(ParametersEnum.TITLE).value,
    }
    context['search_action'] = reverse(APP_NAME+":search")
    return context
class SalaryViews(View):
    def employee_salary(self,request,*args, **kwargs):
        employee_salary=EmployeeSalaryRepo(request=request).employee_salary(*args, **kwargs)
        if employee_salary is None:
            raise Http404
        context=getContext(request=request)
        context['employee_salary']=employee_salary
        negative_lines=employee_salary.negative_lines()
        positive_lines=employee_salary.positive_lines()
        context['negative_lines']=negative_lines
        context['positive_lines']=positive_lines
        return render(request,TEMPLATE_ROOT+"employee-salary.html",context)
    def print(self,request,*args, **kwargs):
        employee_salary=EmployeeSalaryRepo(request=request).employee_salary(*args, **kwargs)
        if employee_salary is None:
            raise Http404
        context=getContext(request=request)
        context['employee_salary']=employee_salary
        negative_lines=employee_salary.negative_lines()
        positive_lines=employee_salary.positive_lines()
        context['negative_lines']=negative_lines
        context['positive_lines']=positive_lines
        return render(request,TEMPLATE_ROOT+"print.html",context)

    def salary_line(self,request,*args, **kwargs):
        employee_salary=EmployeeSalaryRepo(request=request).salary_line(*args, **kwargs)
        context=getContext(request=request)
        context['employee_salary']=employee_salary
        negative_lines=employee_salary.negative_lines()
        positive_lines=employee_salary.positive_lines()
        context['negative_lines']=negative_lines
        context['positive_lines']=positive_lines
        return render(request,TEMPLATE_ROOT+"salary-line.html",context)

class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        employee_salaries=EmployeeSalaryRepo(request=request).list(*args, **kwargs)
        context['employee_salaries']=employee_salaries
        if request.user.has_perm(APP_NAME+".add_employeesalary"):
            context['add_employee_salary_form']=AddEmployeeSalaryForm()
            context['month_names']=PERSIAN_MONTH_NAMES
            employees=EmployeeRepo(request=request).list()
            context['employees']=employees
        return render(request,TEMPLATE_ROOT+"index.html",context)
    def search(self,request,*args, **kwargs):
        context=getContext(request=request)
        employee_salaries=EmployeeSalaryRepo(request=request).list()
        context['employee_salaries']=employee_salaries
        return render(request,TEMPLATE_ROOT+"search.html",context)