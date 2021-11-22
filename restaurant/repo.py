from django.http import request
from django.utils import timezone
from .apps import APP_NAME
from .models import Guest,Food, Meal, ReservedMeal
from authentication.repo import ProfileRepo


class GuestRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        self.me = None
        self.objects = Guest.objects.filter(pk=0)
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(request=self.request).me
        if self.profile is not None:
            self.me=Guest.objects.filter(profile_id=self.profile.id).first()
            self.objects=Guest.objects
    def guest(self, *args, **kwargs):
        
        if 'guest_id' in kwargs:
            pk=kwargs['guest_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

  

class MealRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Meal.objects
    def meal(self, *args, **kwargs):
        
        if 'meal_id' in kwargs:
            pk=kwargs['meal_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        # if 'is_reserved' in kwargs:
        #     guest=GuestRepo(request=self.request).me
        #     for meal in objects.all():
        #         meal.is_reserved(guest_id=guest.id)
        #         print(meal.reserved)
        # for meal in objects.all():
        #     print(meal.reserved)
        return objects.all()


  
    

    

class ReservedMealRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=ReservedMeal.objects


    def reserve_meal(self, *args, **kwargs):
        meal_id=kwargs['meal_id'] if 'meal_id' in kwargs else None
        guest_id=kwargs['guest_id'] if 'guest_id' in kwargs else None
        if guest_id is None:
            guest=GuestRepo(request=self.request).me
            if guest is not None:
                guest_id=guest.id
        if guest_id is None or meal_id is None:
            return None
        reserved_meal=ReservedMeal.objects.filter(meal_id=meal_id).filter(guest_id=guest_id).first()
        if reserved_meal is not None:
            return
        # guest=GuestRepo(request=self.request).guest(*args, **kwargs)
        # if guest is None:
        #     return None
        reserved_meal = ReservedMeal()
        reserved_meal.guest_id=guest_id
        reserved_meal.meal_id=meal_id
        reserved_meal.save()
        return reserved_meal
  

    def reserved_meal(self, *args, **kwargs):
        if 'meal_id' in kwargs and 'guest_id' in kwargs:
            meal_id=kwargs['meal_id']
            guest_id=kwargs['guest_id'] 
            if guest_id is None :
                guest=GuestRepo(request=self.request).me
                if guest is not None:
                    guest_id=guest.id
            return self.objects.filter(meal_id=meal_id).filter(guest_id= guest_id).first()
        pk=0
        if 'reserved_meal_id' in kwargs:
            pk=kwargs['reserved_meal_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'meal_id' in kwargs:
            objects = objects.filter(meal_id=kwargs['meal_id'])
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()
    def serve_meal(self, *args, **kwargs):
        reserved_meal=self.reserved_meal(*args, **kwargs)
        if reserved_meal is None or reserved_meal.date_served is not None:
            return
        reserved_meal.date_served=timezone.now()
        reserved_meal.save() 
        return reserved_meal
            
    def unserve_meal(self, *args, **kwargs):
        reserved_meal=self.reserved_meal(*args, **kwargs)
        if reserved_meal is None or reserved_meal.date_served is None:
            return
        reserved_meal.date_served=None
        reserved_meal.save() 
        return reserved_meal
            
  
    def unreserve_meal(self, *args, **kwargs):
        reserved_meal=self.reserved_meal(*args, **kwargs)
        if reserved_meal is None:
            return
        meal=reserved_meal.meal
        reserved_meal.delete()
        return meal

class FoodRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Food.objects
    def food(self, *args, **kwargs):
        pk=0
        if 'food_id' in kwargs:
            pk=kwargs['food_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()


    def add_food(self, *args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_food"):
            return
        food=Food()
        if 'title' in kwargs:
            food.title = kwargs['title']
        food.save()
        return food
  