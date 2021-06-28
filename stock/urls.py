from django import apps
from .apps import APP_NAME
from django.urls import path
from . import views,apis

app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('stock/<int:pk>/',views.StockViews().stock,name="stock"),
    path('agent/<int:agent_id>/',views.StockViews().agent,name="agent"),
    path('download/<int:pk>/',views.DocumentViews().get_download_response,name="get_download_response"),

    path('search/',views.BasicViews().search,name="search"),
    path('add_document/',apis.DocumentApi().add_document,name="add_document"),
    path('add_payment/',apis.PaymentApi().add_payment,name="add_payment"),
]
