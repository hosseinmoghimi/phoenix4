from .apps import APP_NAME
from . import views,apis
from django.urls import path,include
app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name="home"),
    path("api/",include(APP_NAME+'.apis')),

    path("product/<int:pk>/",views.ProductViews().product,name="product"),
    path("category/<int:pk>/",views.CategoryViews().category,name="category"),

    
]
