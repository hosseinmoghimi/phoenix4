from django.contrib import admin

from restaurant.models import Food, Guest, Meal, ReservedMeal
admin.site.register(Food)
admin.site.register(Guest)
admin.site.register(Meal)
admin.site.register(ReservedMeal)