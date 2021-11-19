from restaurant import apis
from .apps import APP_NAME
from django.urls import path
from . import views
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('food/<int:pk>/',views.FoodViews().food,name="food"),
    path('foods/',views.FoodViews().foods,name="foods"),

    path('add_food/',apis.FoodApi().add_food,name="add_food"),
]
