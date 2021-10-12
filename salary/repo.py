from django.utils import timezone
from salary.models import EmployeeSalary, SalaryLine
from utility.persian import PERSIAN_MONTH_NAMES
from .apps import APP_NAME
from authentication.repo import ProfileRepo

class EmployeeSalaryRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = EmployeeSalary.objects
        self.me=ProfileRepo(user=self.user).me

    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'employee_id' in kwargs:
            employee_id=kwargs['employee_id']
            objects=objects.filter(employee_id=employee_id)
        if 'employee' in kwargs:
            employee=kwargs['employee']
            objects=objects.filter(employee=employee)
        return objects.order_by('-year','-month')
      
    def add_employee_salary(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_employeesalary"):
            return
        employee_id=kwargs['employee_id'] if 'employee_id' in kwargs else 0
        month_name=kwargs['month_name'] if 'month_name' in kwargs else ""
        date_paid=kwargs['date_paid'] if 'date_paid' in kwargs else None
        year=kwargs['year'] if 'year' in kwargs else 0
        month=kwargs['month'] if 'month' in kwargs else 0
        employee_salary=EmployeeSalary()
        employee_salary.employee_id=employee_id
        employee_salary.year=year
        if date_paid is not None:
            employee_salary.date_paid=date_paid
        else:
            employee_salary.date_paid=timezone.now()

        if month is not None and not month=="" and month>0 and month<13:
            employee_salary.month=month
            employee_salary.month_name=PERSIAN_MONTH_NAMES[month-1]
        if month_name is not None and not month_name=="":
            i=1
            for mn in PERSIAN_MONTH_NAMES:
                if mn==month_name :
                    employee_salary.month=i
                    employee_salary.month_name=month_name
                i+=1

        employee_salary.save()
        return employee_salary

    def employee_salary(self,*args, **kwargs):
        pk=0
        if 'employee_salary_id' in kwargs:
            pk=kwargs['employee_salary_id']
            return self.objects.filter(pk=pk).first()
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
        return self.objects.filter(pk=pk).first()




class SalaryLineRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = SalaryLine.objects
        self.me=ProfileRepo(user=self.user).me

    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'employee_salary_id' in kwargs:
            employee_salary_id=kwargs['employee_salary_id']
            objects=objects.filter(employee_salary_id=employee_salary_id)
        return objects
      
    def add_salary_line(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_salary_line"):
            return
        employee_salary_id=kwargs['employee_salary_id'] if 'employee_salary_id' in kwargs else 0
        amount=kwargs['amount'] if 'amount' in kwargs else ""
        title=kwargs['title'] if 'title' in kwargs else None
        direction=kwargs['direction'] if 'direction' in kwargs else 0
        
        salary_line=SalaryLine()
        salary_line.employee_salary_id=employee_salary_id
        salary_line.amount=amount
        salary_line.title=title
        salary_line.direction=direction
        
        salary_line.save()
        return salary_line

    
    def salary_line(self,*args, **kwargs):
        objects=self.objects.all()
        pk=0
        if 'salaryline_id' in kwargs:
            pk=kwargs['salaryline_id']
        if 'salary_line_id' in kwargs:
            pk=kwargs['salary_line_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return objects.filter(pk=pk).first()

