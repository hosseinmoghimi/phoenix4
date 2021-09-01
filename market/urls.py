from market import apis
from .apps import APP_NAME
from . import views,apis
from django.urls import path,include
app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name="home"),
    path("product/<int:pk>/",views.ProductViews().product,name="product"),
    path("category/<int:pk>/",views.CategoryViews().category,name="category"),

    path("api/products/<int:category_id>/",apis.ProductApi().products,name="products"),
    path("api/add_product/",apis.ProductApi().add_product,name="add_product"),
    
]
