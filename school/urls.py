from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    
    path("",views.BasicViews().home,name="home"),
    path("school/<int:pk>/",views.SchoolViews().school,name="school"),
    path("student/<int:pk>/",views.StudentViews().student,name="student"),
    path("teacher/<int:pk>/",views.TeacherViews().teacher,name="teacher"),
    path("book/<int:pk>/",views.BookViews().book,name="book"),
    path("session/<int:pk>/",views.SessionViews().session,name="session"),
    path("classroom/<int:pk>/",views.SchoolViews().classroom,name="classroom"),
    path("activecourse/<int:pk>/",views.CourseViews().active_course,name="activecourse"),
    path("course/<int:pk>/",views.CourseViews().course,name="course"),
]
