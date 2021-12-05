from .apps import APP_NAME
from . import views,apis
from django.urls import path

app_name=APP_NAME
urlpatterns=[
    path("", views.BasicViews().home, name="home"),
    path("resume/<int:pk>/", views.BasicViews().resume, name="resume"),
    path("resume_category/<int:pk>/", views.BasicViews().resume_category, name="resumecategory"),
]
