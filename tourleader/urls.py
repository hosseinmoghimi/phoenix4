from .apps import APP_NAME
from . import views,apis
from django.urls import path



app_name=APP_NAME
urlpatterns = [
    path("",views.BasicView().home,name="home"),
    path("food/<int:pk>/",views.FoodViews().food,name="food"),
    path("foods/",views.FoodViews().foods,name="foods"),
    path("add_food/",apis.FoodApi().add_food,name="add_food"),
]
