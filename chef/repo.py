from django import forms
from .apps import APP_NAME
from .models import Food
from authentication.repo import ProfileRepo

class FoodRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Food.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def food(self, *args, **kwargs):
        if 'food_id' in kwargs:
            return self.objects.filter(pk= kwargs['food_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
            
    def add_food(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_food"):
            return
        food=Food()
        if 'title' in kwargs:
            food.title= kwargs['title']
        food.save()
        return food