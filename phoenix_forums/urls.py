from .apps import APP_NAME
from . import views,apis
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('forum/<int:pk>/',views.ForumViews().forum,name='forum'),
]
