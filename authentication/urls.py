from django.urls import path
from . import views,apis,apk_apis
from .apps import APP_NAME, AuthenticationConfig

app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('register/',views.AuthenticationViews().register,name='register'),
    path('reset_password/<int:profile_id>/',views.AuthenticationViews().reset_password,name='reset_password_view'),
    path('reset_password/',views.AuthenticationViews().reset_password,name='reset_password'),
    path('login_as_user/',views.AuthenticationViews().login_as_user,name="login_as_user"),
    path('profiles/',views.AuthenticationViews().profiles,name='profiles'),
    path('logout/',views.AuthenticationViews().logout,name='logout'),
    path('profile2/<int:pk>/',views.ProfileViews().profile2,name="profile2"),
    path('profile/<int:pk>/',views.ProfileViews().profile,name="profile"),
    path('dashboard/<int:pk>/',views.ProfileViews().dashboard,name="dashboard"),
    path('edit_profile/<int:profile_id>/',views.ProfileViews().edit_profile,name="edit_profile_view"),
    # path(r'^login/(?P<next>\w{0,50})/$', views.AuthenticationViews().login2,name="login_next"),
    path("login/",views.AuthenticationViews().login,name="login"),
    path('edit_profile_/<int:profile_id>/',apis.ProfileApi().edit_profile,name="edit_profile"),
    path('add_profile/',apis.ProfileApi().add_profile,name="add_profile"),
    path('membership_requests/',views.MembershipRequestViews().membership_requests,name="membership_requests"),
    path('membership_requests/<app_name>/',views.MembershipRequestViews().membership_requests,name="membership_requests_app"),
    
    path('handle_membership_request/',apis.MembershipRequestApi().handle_membership_request,name="handle_membership_request"),
    path('add_membership_request/',apis.MembershipRequestApi().add_membership_request,name="add_membership_request"),
    path('upload_profile_image/<int:profile_id>/',views.ProfileViews().upload_profile_image,name="upload_profile_image"),


    # path('apk-api/login_/',apk_apis.ProfileApi().login,name="apk_login"),
    path('apk-api/login/',apk_apis.CustomAuthToken.as_view()),
    path('apk-api/edit_profile/<int:profile_id>/',apk_apis.EditProfile.as_view()),
]
