from django.urls import path
from . import views,apis
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('player/<int:pk>/',views.BasicViews().player,name='player'),
    path('god/<int:pk>/',views.BasicViews().god,name='god'),
    path('game/<int:pk>/',views.BasicViews().game,name='game'),

    
    path('add_player/',apis.BasicApi().add_player,name='add_player'),
]
