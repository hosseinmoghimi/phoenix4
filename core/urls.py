from django.urls import path
from . import apis,views
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name='home'),
    path("add_page",apis.BasicApi().add_page,name='add_page'),
    path("page/<int:pk>/",views.PageViews().page,name='page'),
]
