from authentication.repo import ProfileRepo
from django.db.models.base import Model
from django.db import models 
from core import repo as CoreRepo
from .models import *
from django.utils import timezone
class AnimalRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Animal.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def add_new_animal(self,*args, **kwargs):
        
        if self.user.has_perm(APP_NAME+".add_animal"):
            category=AnimalCategoryEnum.SHEEP
            price=0
            weight=0
            tag="0000"
            saloon_id=0
            enter_date=timezone.now()
            if 'category' in kwargs:
                category=kwargs['category']
            if 'price' in kwargs:
                price=kwargs['price']
            if 'weight' in kwargs:
                weight=kwargs['weight']
            if 'tag' in kwargs:
                tag=kwargs['tag']
            if 'saloon_id' in kwargs:
                saloon_id=kwargs['saloon_id']
            if 'enter_date' in kwargs:
                enter_date=kwargs['enter_date']

            animal=Animal()
            animal.buy_price=price
            animal.category=category
            animal.tag=tag
            animal.enter_date=enter_date
            animal.weight=weight
            animal.save()

            employee=EmployeeRepo(user=self.user).me
            animal_in_saloon=AnimalInSaloon()
            animal_in_saloon.animal=animal
            animal_in_saloon.employee=employee
            animal_in_saloon.saloon_id=saloon_id
            animal_in_saloon.enter_date=enter_date
            animal_in_saloon.animal_price=price
            animal_in_saloon.animal_weight=weight
            animal_in_saloon.save()
            return animal_in_saloon
                
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
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Food.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def food(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None




class DrugRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Drug.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def drug(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None


class FarmRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Farm.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def farm(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None

class SaloonFoodRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=SaloonFood.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def saloon_food(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None

class SaloonRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Saloon.objects
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
    def enter_animal_to_saloon(self,*args, **kwargs):
        saloon_id=0
        animal_id=0
        animal_price=0
        animal_weight=0
        enter_date=timezone.now()
        employee=EmployeeRepo(user=self.user).me

        if 'animal_id' in kwargs:
            animal_id=kwargs['animal_id']
        if 'animal_price' in kwargs:
            animal_price=kwargs['animal_price']
        if 'animal_weight' in kwargs:
            animal_weight=kwargs['animal_weight']
        if 'saloon_id' in kwargs:
            saloon_id=kwargs['saloon_id']
        if 'enter_date' in kwargs:
            enter_date=kwargs['enter_date']


        saloon=self.saloon(saloon_id)
        for animal_in_saloon in AnimalInSaloon.objects.filter(animal_id=animal_id).filter(exit_date=None):
            from datetime import timedelta
            animal_in_saloon.exit_date=enter_date+timedelta(seconds=-1)
            animal_in_saloon.save()

        animal_in_saloon=AnimalInSaloon(animal_id=animal_id,employee=employee,saloon=saloon,enter_date=enter_date,animal_price=animal_price,animal_weight=animal_weight)
        animal_in_saloon.save()

        animal=Animal.objects.filter(pk=animal_id).first()
        animal.weight=animal_weight
        animal.save()
        log=Log(animal_id=animal_id,saloon=saloon,farm=saloon.farm,employee=employee)
        log.save()
        return animal_in_saloon

class FarmRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Farm.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def farm(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None


class DoctorRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Doctor.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def doctor(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None




class EmployeeRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Employee.objects
        self.profile=ProfileRepo(user=self.user).me
        self.me=Employee.objects.filter(profile=self.profile).first()
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def employee(self,*args, **kwargs):
        if 'employee_id' in kwargs:
            pk=kwargs['employee_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

class LogRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Log.objects
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


