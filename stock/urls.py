from django import apps
from .apps import APP_NAME
from django.urls import path
from . import views,apis

app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('stock/<int:pk>/',views.StockViews().stock,name="stock"),
    path('agent/<int:agent_id>/',views.StockViews().agent,name="agent"),
]
