from django.urls import path
from . import views,apis
from .apps import APP_NAME
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name="home"),
    path("message/<int:pk>/",views.MessageViews().message,name="message"),
    path("channel/<int:pk>/",login_required(views.ChannelViews().channel),name="channel"),
    # path("event/<int:pk>/",views.EventViews().event,name="event"),
    path("member/<int:pk>/",views.ChannelViews().member,name="member"),

    
    path("send_message/",apis.ChannelApi().send_message,name="send_message"),
]
