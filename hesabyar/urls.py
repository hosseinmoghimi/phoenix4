from django.urls import path
from .apps import APP_NAME
from django.contrib.auth.decorators import login_required
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    path('search/',login_required(views.BasicViews().search),name="search"),
    path('cheques/',login_required(views.ChequeViews().cheques),name="cheques"),
    # path('profile_financial_account/<pk>/',login_required(views.ReportViews().profile_financial_account),name="profile_financial_account"),
    path('service/<int:pk>/',login_required(views.ServiceViews().service),name="service"),
    path('payment_financial_document/<int:pk>/',login_required(views.FinancialDocumentViews().payment_financial_document),name="paymentfinancialdocument"),
    path('products/',login_required(views.ProductViews().products),name="products"),
    path('services/',login_required(views.ServiceViews().services),name="services"),
    path('edit_invoice/<int:pk>/',login_required(views.InvoiceViews().edit_invoice),name="edit_invoice"),
    path('invoice_print/<int:pk>/',login_required(views.InvoiceViews().invoice_print),name="invoice_print"),
    path('cheque/<int:pk>/',login_required(views.ChequeViews().cheque),name="cheque"),
    path('new_payment/',login_required(views.PaymentViews().new_payment),name="new_payment"),
    path('payments/',login_required(views.PaymentViews().payments),name="payments"),
    path('payment/<int:pk>/',login_required(views.PaymentViews().payment),name="payment"),
    
    
    path('sell/',login_required(views.InvoiceViews().sell),name="sell"),
    path('ware_house_sheet/<int:pk>/',login_required(views.WareHouseSheetViews().ware_house_sheet),name="warehousesheet"),
    path('ware_house/<int:pk>/',login_required(views.WareHouseViews().ware_house),name="warehouse"),
    path('product/<int:pk>/',login_required(views.ProductViews().product),name="product"),
    path('financial_documents/',login_required(views.FinancialDocumentViews().financial_documents),name="financial_documents"),
    path('store/<int:pk>/',login_required(views.StoreViews().store),name="store"),
    path('invoice/<int:pk>/',login_required(views.InvoiceViews().invoice),name="invoice"),
    path('invoices/',login_required(views.InvoiceViews().invoices),name="invoices"),
    path('invoice_financial_document/<int:pk>/',login_required(views.FinancialDocumentViews().invoice_financial_document),name="invoicefinancialdocument"),
    path('financial_account/<int:pk>/',login_required(views.ReportViews().financial_account),name="financial_account"),
    path('financial_document/<int:pk>/',login_required(views.ReportViews().financial_document),name="financialdocument"),
    path('bank_account/<int:pk>/',login_required(views.BankAccountViews().bank_account),name="bank_account"),
    path('tag/<int:pk>/',login_required(views.BasicViews().tag),name="tag"),
    path('financial_document_category/<int:pk>/',login_required(views.ReportViews().financial_document_category),name="financial_document_category"),


    path('add_financial_document/',login_required(apis.BasicApi().add_financial_document),name="add_financial_document"),
    path('edit_invoice_post/',login_required(apis.BasicApi().edit_invoice),name="edit_invoice_post"),
    path('add_cheque/',login_required(apis.CheuqeApi().add_cheque),name="add_cheque"),
    path('add_payment/',login_required(apis.PaymentApi().add_payment),name="add_payment"),
    
]
