from django.urls import path
from . import views,apis
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('player/<int:pk>/',views.BasicViews().player,name='player'),
    path('game1/',views.BasicViews().game1,name='game1'),
    path('game2/',views.BasicViews().game2,name='game2'),
    path('shuffle_game/',views.BasicViews().shuffle_game,name='shuffle_game'),
    path('new_vote/',views.BasicViews().new_vote,name='new_vote'),
    path('start_game/',views.BasicViews().start_game,name='start_game'),
    path('day_accuse/',views.BasicViews().day_accuse,name='day_accuse'),    
    path('god/<int:pk>/',views.BasicViews().god,name='god'),
    path('game_day/<int:pk>/',views.BasicViews().game_day,name='game_day'),
    path('game_night/<int:pk>/',views.BasicViews().game_night,name='game_night'),
    path('game/<int:pk>/',views.BasicViews().game,name='game'),
    path('role/<int:pk>/',views.BasicViews().role,name='role'),
    path('change_game_state/',views.BasicViews().change_game_state,name='change_game_state'),
    path('game_role/<int:game_role_id>/',views.BasicViews().game_role,name='game_role'),

    
    path('add_all_vote/',apis.BasicApi().add_all_vote,name='add_all_vote'),
    path('start_game_night/',apis.BasicApi().start_game_night,name='start_game_night'),
    path('start_game_day/',apis.BasicApi().start_game_day,name='start_game_day'),
    path('add_player/',apis.BasicApi().add_player,name='add_player'),
]
