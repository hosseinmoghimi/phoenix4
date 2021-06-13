from . import views,apis
from .apps import APP_NAME
from django.urls import path


app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name="home"),
    path("resume_category/<int:pk>/",views.ResumeViews().resume_category,name="resumecategory"),
]
