from .apps import APP_NAME
from django.urls import path
from . import apis,views
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('search/',views.BasicViews().search,name='search'),
    path('employee/<int:employee_id>/',views.BasicViews().home,name='employee'),
    path('employee_salary/<int:employee_id>/',views.SalaryViews().employee_salary,name='employee_salary'),
    path('employee__salary/<int:pk>/',views.SalaryViews().employee_salary,name='employeesalary'),
    path('print/<int:pk>/',views.SalaryViews().print,name='print'),
    path('salaryline/<int:pk>/',views.SalaryViews().salary_line,name='salaryline'),


    path('add_employee_salary/',apis.EmployeeSalaryApi().add_employee_salary,name="add_employee_salary"),
]
