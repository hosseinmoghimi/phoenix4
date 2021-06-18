from django.urls import path
from . import apis,views
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name='home'),
    path("add_page",apis.BasicApi().add_page,name='add_page'),
    path("add_page_document",apis.BasicApi().add_page_document,name='add_page_document'),
    
    path("delete_page_comment",apis.BasicApi().delete_page_comment,name='delete_page_comment'),
    path("add_page_comment",apis.BasicApi().add_page_comment,name='add_page_comment'),
    path("add_page_image",apis.BasicApi().add_page_image,name='add_page_image'),
    path("add_page_link",apis.BasicApi().add_page_link,name='add_page_link'),
    path("page/<int:pk>/",views.PageViews().page,name='page'),
    path('page-chart/<int:pk>/',views.PageViews().page_chart,name="page_chart"),
    path("download/<int:pk>/",views.PageViews().download,name='download'),
]
