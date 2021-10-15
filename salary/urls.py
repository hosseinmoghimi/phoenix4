from .apps import APP_NAME
from django.urls import path
from . import apis,views

from django.contrib.auth.decorators import login_required


app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name='home'),
    path('search/',login_required(views.BasicViews().search),name='search'),
    path('employee/<int:employee_id>/',login_required(views.BasicViews().home),name='employee'),
    path('employee_salary/<int:employee_id>/',login_required(views.SalaryViews().employee_salary),name='employee_salary'),
    path('employee__salary/<int:pk>/',login_required(views.SalaryViews().employee_salary),name='employeesalary'),
    path('print/<int:pk>/',login_required(views.SalaryViews().print),name='print'),
    path('salary_line/<int:pk>/',login_required(views.SalaryViews().salary_line),name='salaryline'),
    path('work_group/<int:pk>/',login_required(views.WorkGroupViews().work_group),name='workgroup'),
    path('work_site/<int:pk>/',login_required(views.WorkSiteViews().work_site),name='worksite'),


    path('add_employee_salary/',login_required(apis.EmployeeSalaryApi().add_employee_salary),name="add_employee_salary"),
    path('add_salary_line/',login_required(apis.EmployeeSalaryApi().add_salary_line),name="add_salary_line"),
]
