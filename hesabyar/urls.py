from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('profile_financial_account/<pk>/',views.ReportViews().profile_financial_account,name="profile_financial_account"),
    path('financial_account/<pk>/',views.ReportViews().financial_account,name="financial_account"),
    path('financial_document/<pk>/',views.ReportViews().financial_document,name="financialdocument"),
    path('tag/<pk>/',views.BasicViews().tag,name="tag"),
    path('add_financial_document/',apis.BasicApi().add_financial_document,name="add_financial_document"),
    path('financial_document_category/<pk>/',views.ReportViews().financial_document_category,name="financial_document_category"),


]
