from resume.apps import APP_NAME
from . import views,apis
from django.urls import path


app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('<int:profile_id>/<int:language_index>/',views.BasicViews().home,name="resume_index_language"),
    path('<int:profile_id>/',views.BasicViews().home,name="resume_index"),
    path('portfolio/<int:pk>/',views.PortfolioViews().portolio,name="portfolio"),
    path('resume_fact/<int:pk>/',views.BasicViews().portfolio,name="resumefact"),
    path('resume_skill/<int:pk>/',views.BasicViews().portfolio,name="resumeskill"),
    path('portfolio/<int:pk>/',views.BasicViews().portfolio,name="resumeportfolio"),
    path('service/<int:pk>/',views.BasicViews().resume_service,name="resumeservice"),
    path('resume/<int:pk>/',views.BasicViews().resume,name="resume"),
    path('add_resume_item/',apis.BasicApi().add_resume_item,name="add_resume_item"),
    path('add_resume_fact/',apis.BasicApi().add_resume_fact,name="add_resume_fact"),
    path('add_resume_skill/',apis.BasicApi().add_resume_skill,name="add_resume_skill"),

    path('add_contact_message/',apis.BasicApi().add_contact_message,name="add_contact_message"),
]