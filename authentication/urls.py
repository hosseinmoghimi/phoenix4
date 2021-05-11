from django.urls import path
from . import views,apis
from .apps import APP_NAME

app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('profile/<int:pk>/',views.ProfileViews().profile,name="profile"),
]
