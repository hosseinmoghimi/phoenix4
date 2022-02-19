from django.urls import path
from .apps import APP_NAME
from django.contrib.auth.decorators import login_required
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    
    path('add_store_price/',login_required(views.ProductViews().add_store_price),name="add_store_price"),
    path('bank_account/<int:pk>/',login_required(views.BankAccountViews().bank_account),name="bank_account"),
    path('bank_accounts/',login_required(views.BankAccountViews().bank_accounts),name="bank_accounts"),
    path('banks/',login_required(views.BankViews().banks),name="banks"),
    path('buy/',login_required(views.InvoiceViews().buy),name="buy"),
    path('cheque/<int:pk>/',login_required(views.ChequeViews().cheque),name="cheque"),
    path('cheques/',login_required(views.ChequeViews().cheques),name="cheques"),
    path('cost/<int:pk>/',login_required(views.CostViews().cost),name="cost"),
    path('costs/',login_required(views.CostViews().costs),name="costs"),
    path('edit_invoice/<int:pk>/',login_required(views.InvoiceViews().edit_invoice),name="edit_invoice"),
    path('financial_account/<int:pk>/',login_required(views.FinancialAccountViews().financial_account),name="financial_account"),
    path('financial_accounts/',login_required(views.FinancialAccountViews().financial_accounts),name="financial_accounts"),
    path('financial_account_print/<int:pk>/',login_required(views.FinancialAccountViews().financial_account_print),name="financial_account_print"),
    path('financial_document/<int:pk>/',login_required(views.FinancialDocumentViews().financial_document),name="financialdocument"),
    path('financial_documents/',login_required(views.FinancialDocumentViews().financial_documents),name="financial_documents"),
    path('financial_document_category/<int:pk>/',login_required(views.FinancialDocumentViews().financial_document_category),name="financial_document_category"),
    path('guarantee/<int:pk>/',login_required(views.GuaranteeViews().guarantee),name="guarantee"),
    path('guarantees/',login_required(views.GuaranteeViews().guarantees),name="guarantees"),
    path('invoice/<int:pk>/',login_required(views.InvoiceViews().invoice),name="invoice"),
    path('invoices/',login_required(views.InvoiceViews().invoices),name="invoices"),
    path('invoice_deliver/<int:pk>/',login_required(views.InvoiceViews().invoice_deliver),name="invoice_deliver"),
    path('invoice_financial_document/<int:pk>/',login_required(views.FinancialDocumentViews().invoice_financial_document),name="invoicefinancialdocument"),
    path('invoice_guarantees/<int:pk>/',login_required(views.InvoiceViews().invoice_guarantees),name="invoice_guarantees"),
    path('invoice_print/<int:pk>/',login_required(views.InvoiceViews().invoice_print),name="invoice_print"),
    path('new_cost/',login_required(views.CostViews().new_cost),name="new_cost"),
    path('new_payment/',login_required(views.PaymentViews().new_payment),name="new_payment"),
    path('new_wage/',login_required(views.WageViews().new_wage),name="new_wage"),
    path('payment/<int:pk>/',login_required(views.PaymentViews().payment),name="payment"),
    path('payments/',login_required(views.PaymentViews().payments),name="payments"),
    path('product/<int:pk>/',(views.ProductViews().product),name="product"),
    path('products/',login_required(views.ProductViews().products),name="products"),
    path('report/<int:financial_account_id>/',login_required(views.ReportViews().report),name="report"),
    path('report_year/<int:financial_account_id>/<int:year>/',login_required(views.ReportViews().report_year),name="report_year"),
    
    path('search/',login_required(views.BasicViews().search),name="search"),
    path('sell/',login_required(views.InvoiceViews().sell),name="sell"),
    path('service/<int:pk>/',login_required(views.ServiceViews().service),name="service"),
    path('services/',login_required(views.ServiceViews().services),name="services"),
    path('spends/',login_required(views.SpendViews().spends),name="spends"),
    path('store/<int:pk>/',login_required(views.StoreViews().store),name="store"),
    path('stores/',login_required(views.StoreViews().stores),name="stores"),
    path('transaction_category/<int:pk>/',login_required(views.TransactionViews().transaction_category),name="transactioncategory"),
    path('transactions/',login_required(views.TransactionViews().transactions),name="transactions"),
    path('tag/<int:pk>/',login_required(views.BasicViews().tag),name="tag"),
    path('wage/<int:pk>/',login_required(views.WageViews().wage),name="wage"),
    path('wages/',login_required(views.WageViews().wages),name="wages"),
    path('ware_house/<int:pk>/',login_required(views.WareHouseViews().ware_house),name="warehouse"),
    path('ware_houses/',login_required(views.WareHouseViews().ware_houses),name="ware_houses"),
    path('ware_house_print/<int:pk>/',login_required(views.WareHouseViews().ware_house_print),name="ware_house_print"),
    path('ware_house_sheet/<int:pk>/',login_required(views.WareHouseSheetViews().ware_house_sheet),name="warehousesheet"),
    # path('profile_financial_account/<pk>/',login_required(views.ReportViews().profile_financial_account),name="profile_financial_account"),
    
    
    
    


    path('add_transaction_link/',login_required(apis.TransactionApi().add_transaction_link),name="add_transaction_link"),
    path('add_transaction_document/',login_required(apis.TransactionApi().add_transaction_document),name="add_transaction_document"),
    path('add_cost/',login_required(apis.CostApi().add_cost),name="add_cost"),
    path('add_wage/',login_required(apis.WageApi().add_wage),name="add_wage"),
    path('add_financial_document/',login_required(apis.BasicApi().add_financial_document),name="add_financial_document"),
    path('edit_invoice_post/',login_required(apis.InvoiceApi().edit_invoice),name="edit_invoice_post"),
    path('add_cheque/',login_required(apis.CheuqeApi().add_cheque),name="add_cheque"),
    path('add_payment/',login_required(apis.PaymentApi().add_payment),name="add_payment"),
    path('change_warehouse_sheet_state/',login_required(apis.WareHouseSheetApi().change_warehouse_sheet_state),name="change_warehouse_sheet_state"),
    
]
