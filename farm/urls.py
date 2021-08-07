from django.urls import path,include
from .apps import APP_NAME
from . import views,apis

app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('search/',views.BasicViews().search,name="search"),
    path('animal/<int:pk>/',views.BasicViews().animal,name="animal"),
    path('animals/',views.BasicViews().animals,name="animals"),
    path('saloonfood/<int:pk>/',views.BasicViews().saloonfood,name="saloonfood"),
    path('doctor/<int:pk>/',views.BasicViews().doctor,name="doctor"),
    path('employee/<int:pk>/',views.BasicViews().employee,name="employee"),
    path('saloon/<int:pk>/',views.BasicViews().saloon,name="saloon"),
    path('cost/<int:pk>/',views.CostViews().cost,name="cost"),
    path('farm/<int:pk>/',views.BasicViews().farm,name="farm"),
    path('food/<int:pk>/',views.BasicViews().food,name="food"),
    path('drug/<int:pk>/',views.BasicViews().drug,name="drug"),
    path('koshtar/<int:pk>/',views.BasicViews().koshtar,name="koshtar"),

    
    path('enter_animal_to_saloon/',apis.BasicApi().enter_animal_to_saloon,name="enter_animal_to_saloon"),
    path('saloon_daily_report/',apis.BasicApi().saloon_daily_report,name="saloon_daily_report"),
    path('add_animal/',apis.BasicApi().add_animal,name="add_animal"),
    path('add_cost/',apis.BasicApi().add_cost,name="add_cost"),
    path('do_koshtar/',apis.BasicApi().do_koshtar,name="do_koshtar"),
]
