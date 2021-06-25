from authentication.repo import ProfileRepo
from django.db.models.base import Model
from django.db import models 
from core import repo as CoreRepo
from .models import *

class AnimalRepo():
    def __init__(self,user):
        self.objects=Animal.objects
        self.user=user
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def animal(self,*args, **kwargs):
        try:
            if 'pk' in kwargs and not kwargs['pk'] is None:
                return self.objects.get(pk=kwargs['pk'])

            if 'animal_id' in kwargs and not kwargs['animal_id'] is None:
                return self.objects.get(pk=kwargs['animal_id'])

            if 'animal_tag' in kwargs and not kwargs['animal_tag'] is None:
                return self.objects.get(tag=kwargs['animal_tag'])

            if 'tag' in kwargs and not kwargs['tag'] is None:
                return self.objects.get(tag=kwargs['tag'])

        except:
            pass
        return None


    def add(self,name,saloon_id,category,tag):
        if self.user.has_perm(APP_NAME+".add_animal"):
            animal=Animal(name=name,category=category,tag=tag)
            animal.save()


class FoodRepo():
    def __init__(self,user):
        self.objects=Food.objects
        self.user=user
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def food(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None



class DrugRepo():
    def __init__(self,user):
        self.objects=Drug.objects
        self.user=user
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def drug(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None


class FarmRepo():
    def __init__(self,user):
        self.objects=Farm.objects
        self.user=user
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def farm(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None

class SaloonFoodRepo():
    def __init__(self,user):
        self.objects=SaloonFood.objects
        self.user=user
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def saloon_food(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None

class SaloonRepo():
    def __init__(self,user=None):
        self.objects=Saloon.objects
        self.user=user
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def saloon(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None
    def saloon_foods(self,saloon_id,report_date):
        saloon_foods= SaloonFood.objects.filter(saloon_id=saloon_id).filter(food_date__date=report_date.date())
        return saloon_foods
    def animals_in_saloon(self,report_date,saloon_id=None,saloon=None,*args, **kwargs):
        if saloon is None and saloon_id is not None:
            saloon=Saloon.objects.get(pk=saloon_id)
        if saloon is not None:
            ids=[]
            for animal in Animal.objects.all():
                a=animal.current_in_saloon(report_date=report_date)
                if a is not None and a.saloon==saloon:
                    ids.append(a.id)

            animalinsaloon_set=AnimalInSaloon.objects.filter(id__in=ids)
            # animalinsaloon_set=animalinsaloon_set.filter(models.Q(exit_date=None)| models.Q(enter_date__gte=report_date))
            return animalinsaloon_set
    def enter_animal_to_saloon(self,saloon_id,animal_id=None,animal_tag=None,enter_date=None,animal_price=None,animal_weight=None,*args, **kwargs):
        if enter_date is None:
            enter_date=PersianCalendar().date
        saloon=self.saloon(saloon_id)
        animal=AnimalRepo(self.user).animal(animal_id=animal_id,animal_tag=animal_tag)
        # AnimalInSaloon.objects.filter(saloon=saloon).filter(animal=animal).delete()
        for animal_in_saloon in AnimalInSaloon.objects.filter(animal=animal).filter(exit_date=None):
            from datetime import timedelta
            animal_in_saloon.exit_date=enter_date+timedelta(seconds=-1)
            animal_in_saloon.save()
        employee=EmployeeRepo(self.user).me

        a=AnimalInSaloon(animal=animal,employee=employee,saloon=saloon,enter_date=enter_date,animal_price=animal_price,animal_weight=animal_weight)

        a.save()
        employee=EmployeeRepo(self.user).me
        log=Log(animal=animal,saloon=saloon,farm=saloon.farm,employee=employee)
        log.save()

class FarmRepo():
    def __init__(self,user):
        self.objects=Farm.objects
        self.user=user
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def farm(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None


class DoctorRepo():
    def __init__(self,user):
        self.objects=Doctor.objects
        self.user=user
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def doctor(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None


class EmployeeRepo():
    def __init__(self,user):
        self.objects=Employee.objects
        self.user=user
        self.profile=ProfileRepo(user).me
        self.me=Employee.objects.get(profile=self.profile)
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def employee(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None

class LogRepo():
    def __init__(self,user):
        self.objects=Log.objects
        self.user=user
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'animal_id' in kwargs:
            animal_id=kwargs['animal_id']
            objects=objects.filter(animal_id=animal_id)
        if 'saloon_id' in kwargs:
            saloon_id=kwargs['saloon_id']
            objects=objects.filter(saloon_id=saloon_id)
        if 'employee_id' in kwargs:
            employee_id=kwargs['employee_id']
            objects=objects.filter(employee_id=employee_id)
        if 'farm_id' in kwargs:
            farm_id=kwargs['farm_id']
            objects=objects.filter(farm_id=farm_id)
        return objects
    def employee(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None
