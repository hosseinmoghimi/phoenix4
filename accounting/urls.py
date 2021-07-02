from .apps import APP_NAME
from . import views,apis
from django.urls import path


app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('financial_account/<int:pk>/',views.TransactionViews().financial_account,name="financial_account"),
    path('asset/<int:asset_id>/',views.AssetViews().asset,name="asset"),
    path('transaction/<int:pk>/',views.TransactionViews().transaction,name="transaction"),
    path('transactions/<int:financial_account_id>/',views.TransactionViews().transactions,name="transactions"),
   
]