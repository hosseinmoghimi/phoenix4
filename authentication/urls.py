from django.urls import path
from . import views,apis
from .apps import APP_NAME, AuthenticationConfig

app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('profiles/',views.AuthenticationViews().profiles,name='profiles'),
    path('logout/',views.AuthenticationViews().logout,name='logout'),
    path('profile2/<int:pk>/',views.ProfileViews().profile2,name="profile2"),
    path('profile/<int:pk>/',views.ProfileViews().profile,name="profile"),
    path('edit_profile/<int:pk>/',views.ProfileViews().edit_profile,name="edit_profile_view"),
    path("login/",views.AuthenticationViews().login,name="login"),
    path('edit_profile/',apis.ProfileApi().edit_profile,name="edit_profile"),
    path('upload_profile_image/',views.ProfileViews().upload_profile_image,name="upload_profile_image"),
]
