from django.urls import path
from .apps import APP_NAME
from django.contrib.auth.decorators import login_required
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    path('search/',login_required(views.BasicViews().search),name="search"),
    path('profile_financial_account/<pk>/',login_required(views.ReportViews().profile_financial_account),name="profile_financial_account"),
    path('service/<pk>/',login_required(views.ServiceViews().service),name="service"),
    path('payment_financial_document/<pk>/',login_required(views.FinancialDocumentViews().payment_financial_document),name="paymentfinancialdocument"),
    path('products/',login_required(views.ProductViews().products),name="products"),
    path('services/',login_required(views.ServiceViews().services),name="services"),
    path('ware_house_sheet/<pk>/',login_required(views.WareHouseSheetViews().ware_house_sheet),name="warehousesheet"),
    path('ware_house/<pk>/',login_required(views.WareHouseViews().ware_house),name="warehouse"),
    path('product/<pk>/',login_required(views.ProductViews().product),name="product"),
    path('financial_documents/',login_required(views.FinancialDocumentViews().financial_documents),name="financial_documents"),
    path('store/<pk>/',login_required(views.StoreViews().store),name="store"),
    path('invoice/<pk>/',login_required(views.InvoiceViews().invoice),name="invoice"),
    path('invoices/',login_required(views.InvoiceViews().invoices),name="invoices"),
    path('invoice_financial_document/<pk>/',login_required(views.FinancialDocumentViews().invoice_financial_document),name="invoicefinancialdocument"),
    path('financial_account/<pk>/',login_required(views.ReportViews().financial_account),name="financial_account"),
    path('financial_document/<pk>/',login_required(views.ReportViews().financial_document),name="financialdocument"),
    path('bank_account/<pk>/',login_required(views.BankAccountViews().bank_account),name="bank_account"),
    path('tag/<pk>/',login_required(views.BasicViews().tag),name="tag"),
    path('add_financial_document/',login_required(apis.BasicApi().add_financial_document),name="add_financial_document"),
    path('financial_document_category/<pk>/',login_required(views.ReportViews().financial_document_category),name="financial_document_category"),


]
