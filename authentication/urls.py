from django.urls import path
from . import views,apis
from .apps import APP_NAME, AuthenticationConfig

app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('logout/',views.AuthenticationViews().logout,name='logout'),
    path('profile2/<int:pk>/',views.ProfileViews().profile2,name="profile2"),
    path('profile/<int:pk>/',views.ProfileViews().profile,name="profile"),
    path("login/",views.AuthenticationViews().login,name="login"),
]
