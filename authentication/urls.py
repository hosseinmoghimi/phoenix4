from django.urls import path
from . import views,apis
from .apps import APP_NAME, AuthenticationConfig

app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('profile/<int:pk>/',views.ProfileViews().profile,name="profile"),
    path("login/",views.AuthenticationViews().login,name="login"),
]
