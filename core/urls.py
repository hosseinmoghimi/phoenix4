from django.urls import path
from . import apis,views
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name='home'),
    path("add_page",apis.BasicApi().add_page,name='add_page'),
    path("add_page_document",apis.BasicApi().add_page_document,name='add_page_document'),
    path("add_page_link",apis.BasicApi().add_page_link,name='add_page_link'),
    path("page/<int:pk>/",views.PageViews().page,name='page'),
    path("download/<int:pk>/",views.PageViews().download,name='download'),
]
