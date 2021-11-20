from restaurant import apis
from .apps import APP_NAME
from django.urls import path
from . import views
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('food/<int:pk>/',views.FoodViews().food,name="food"),
    path('guest/<int:pk>/',views.GuestViews().guest,name="guest"),
    path('foods/',views.FoodViews().foods,name="foods"),
    path('guests/',views.GuestViews().guests,name="guests"),
    # path('week/<int:year>/<int:month>/<int:day>/',views.MealViews().week,name="week"),
    path('meal/<int:pk>/',views.MealViews().meal,name="meal"),
    path('meals/',views.MealViews().meals,name="meals"),

    path('add_food/',apis.FoodApi().add_food,name="add_food"),
]
