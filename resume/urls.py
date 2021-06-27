from resume.apps import APP_NAME
from . import views
from django.urls import path


app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('<int:profile_id>/',views.BasicViews().home,name="resume_index"),
    path('portfolio/<int:pk>/',views.BasicViews().portfolio,name="resumeportfolio"),
    path('service/<int:pk>/',views.BasicViews().resume_service,name="resumeservice"),
    path('resume/<int:pk>/',views.BasicViews().resume,name="resume"),
]