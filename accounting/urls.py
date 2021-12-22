from .apps import APP_NAME
from . import views,apis
from django.urls import path


from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    path('financial_account/<int:financial_account_id>/',login_required(views.FinancialAccountViews().financial_account),name="financial_account"),
    path('financial_accounts/',login_required(views.FinancialAccountViews().financial_accounts),name="financial_accounts"),
    path('asset/<int:asset_id>/',login_required(views.AssetViews().asset),name="asset"),
    path('assets/',login_required(views.AssetViews().assets),name="assets"),
    path('transaction/<int:pk>/',login_required(views.TransactionViews().transaction),name="transaction"),
    path('transactions/<int:pay_from_id>/<int:pay_to_id>/',login_required(views.TransactionViews().transactions2),name="transactions2"),
    path('money_transaction/<int:pk>/',login_required(views.TransactionViews().money_transaction),name="moneytransaction"),
    path('project_transaction/<int:pk>/',login_required(views.TransactionViews().project_transaction),name="projecttransaction"),
    path('asset_transaction/<int:pk>/',login_required(views.TransactionViews().asset_transaction),name="assettransaction"),
    path('market_order_transaction/<int:pk>/',login_required(views.TransactionViews().market_order_transaction),name="marketordertransaction"),
    path('transactions/<int:financial_account_id>/',login_required(views.TransactionViews().transactions),name="transactions"),
    
    
    
    
    path('add_transaction/',login_required(apis.TransactionApi().add_transaction),name="add_transaction"),
   
]