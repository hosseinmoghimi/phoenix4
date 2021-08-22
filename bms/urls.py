from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('scenario/<int:pk>/',views.BasicViews().scenario,name='scenario'),
    path('feeder/<int:pk>/',views.BasicViews().feeder,name='feeder'),
    path('run_scenario/',apis.BasicApi().run_scenario,name='run_scenario'),
    path('logs/',views.BasicViews().logs,name='logs'),
    path('get_logs/',apis.BasicApi().get_logs,name='get_logs'),
    path('command/<int:pk>/',views.BasicViews().command,name='command'),
    path('relay/<int:pk>/',views.BasicViews().relay,name='relay'),
    path('export/',apis.BasicApi().export,name="export"),
    path('execute_command/',apis.BasicApi().execute_command,name="execute_command"),
    path('add_log_from_client/',apis.add_log_from_client,name="add_log_from_client"),
]
