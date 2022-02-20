from django.shortcuts import render,reverse
from django.http import Http404
from salary.enums import SalaryTitleEnum
from salary.forms import AddEmployeeSalaryForm, AddSalaryLineForm, AddVacationForm
from salary.models import SalaryLine
from salary.repo import EmployeeSalaryRepo, VacationRepo,WorkGroupRepo,WorkSiteRepo
from salary.serializers import VacationSerializer
from .apps import APP_NAME
from django.views import View
from projectmanager.repo import EmployeeRepo
from projectmanager.serializers import EmployeeSerializer2
from core.views import  PageContext,CoreContext
from core.repo import ParameterRepo,PictureRepo,ParametersEnum
import json
from utility.persian import PERSIAN_MONTH_NAMES
TEMPLATE_ROOT="salary/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
 
    context['search_action'] = reverse(APP_NAME+":search")
    return context
class SalaryViews(View):
    def employee_salary(self,request,*args, **kwargs):
        employee_salary=EmployeeSalaryRepo(request=request).employee_salary(*args, **kwargs)
        if employee_salary is None:
            from log.repo import LogRepo
            LogRepo(request=request).add_log(title="Http404 salary views 1") 
            raise Http404
        context=getContext(request=request)
        context['employee_salary']=employee_salary
        negative_lines=employee_salary.negative_lines()
        positive_lines=employee_salary.positive_lines()
        context['negative_lines']=negative_lines
        context['positive_lines']=positive_lines
        if request.user.has_perm(APP_NAME+".add_salaryline"):
            context['add_salary_line_form']=AddSalaryLineForm()
            titles=[]
            for i in SalaryTitleEnum.choices:
                titles.append(i[0])
            context['line_titles']=titles
            context['salary_line_titles']=json.dumps(titles)
        return render(request,TEMPLATE_ROOT+"employee-salary.html",context)

    def print(self,request,*args, **kwargs):
        employee_salary=EmployeeSalaryRepo(request=request).employee_salary(*args, **kwargs)
        if employee_salary is None:
            from log.repo import LogRepo
            LogRepo(request=request).add_log(title="Http404 salary views 2") 
            raise Http404
        context=getContext(request=request)
        context['employee_salary']=employee_salary
        negative_lines=employee_salary.negative_lines()
        positive_lines=employee_salary.positive_lines()
        context['negative_lines']=negative_lines
        context['positive_lines']=positive_lines
        return render(request,TEMPLATE_ROOT+"print.html",context)

    def salary_line(self,request,*args, **kwargs):
        employee_salary=SalaryLine(request=request).salary_line(*args, **kwargs)
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
        vacations=VacationRepo(request=request).list(*args, **kwargs)
        context['vacations']=vacations
        employee=EmployeeRepo(request=request).employee(*args, **kwargs)
        context['employee_salaries']=employee_salaries
        context['employee']=employee
        if request.user.has_perm(APP_NAME+".add_employeesalary"):
            context['add_employee_salary_form']=AddEmployeeSalaryForm()
            context['month_names']=PERSIAN_MONTH_NAMES
            employees=EmployeeRepo(request=request).list()
            context['employees']=employees
        return render(request,TEMPLATE_ROOT+"index.html",context)
    def employee(self,request,*args, **kwargs):
        context=getContext(request=request)
        employee_salaries=EmployeeSalaryRepo(request=request).list(*args, **kwargs)
        vacations=VacationRepo(request=request).list(*args, **kwargs)
        context['vacations']=vacations
        vacations_s=json.dumps(VacationSerializer(vacations,many=True).data)
        context['vacations_s']=vacations_s
        context['add_vacation_form']=AddVacationForm()
        employee=EmployeeRepo(request=request).employee(*args, **kwargs)
        context['employee_salaries']=employee_salaries
        context['employee']=employee
        if request.user.has_perm(APP_NAME+".add_employeesalary"):
            context['add_employee_salary_form']=AddEmployeeSalaryForm()
            context['month_names']=PERSIAN_MONTH_NAMES
            employees=EmployeeRepo(request=request).list()
            context['employees']=employees
        return render(request,TEMPLATE_ROOT+"employee.html",context)
    def search(self,request,*args, **kwargs):
        context=getContext(request=request)
        employee_salaries=EmployeeSalaryRepo(request=request).list()
        context['employee_salaries']=employee_salaries
        return render(request,TEMPLATE_ROOT+"search.html",context)
    

class WorkGroupViews(View):
    def work_group(self,request,*args, **kwargs):
        context=getContext(request=request)
        work_group=WorkGroupRepo(request=request).work_group(*args, **kwargs)
        employees=work_group.employees()
        context['work_group']=work_group
        context['employees']=employees
        context['employees_s']=json.dumps(EmployeeSerializer2(employees,many=True).data)
        context['organization_unit']="a"
        return render(request,TEMPLATE_ROOT+"work-group.html",context)


class VacationViews(View):
    def vacation(self,request,*args, **kwargs):
        vacation=VacationRepo(request=request).vacation(*args, **kwargs)
        context=getContext(request=request)
        context.update(PageContext(request=request,page=vacation))
        context['vacation']=vacation
        return render(request,TEMPLATE_ROOT+"vacation.html",context)


class WorkSiteViews(View):
    def work_site(self,request,*args, **kwargs):
        context=getContext(request=request)
        work_site_repo=WorkSiteRepo(request=request)
        work_site=work_site_repo.work_site(*args, **kwargs)
        if work_site is None:
            work_sites=work_site_repo.list().filter(parent=None)
        else:
            work_sites=work_site.childs()
        context['work_site']=work_site
        context['work_sites']=work_sites
        return render(request,TEMPLATE_ROOT+"work-site.html",context)