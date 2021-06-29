from .apps import APP_NAME
from . import views,apis
from django.urls import path


app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('financial_account/<int:pk>/',views.TransactionViews().financial_account,name="financial_account"),
    path('transaction/<int:pk>/',views.TransactionViews().transaction,name="transaction"),
   
]