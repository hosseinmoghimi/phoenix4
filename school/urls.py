from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    
    path("",views.BasicViews().home,name="home"),
    
    path("search/",views.BasicViews().search,name="search"),


    path("schools/",views.SchoolViews().schools,name="schools"),
    path("school/<int:school_id>/",views.SchoolViews().school,name="school"),
    path("add_school/",apis.SchoolApi().add_school,name="add_school"),

    path("students/",views.StudentViews().students,name="students"),
    path("student/<int:pk>/",views.StudentViews().student,name="student"),
    path("add_student/",apis.StudentApi().add_student,name="add_student"),

    path("teachers/",views.TeacherViews().teachers,name="teachers"),
    path("teacher/<int:pk>/",views.TeacherViews().teacher,name="teacher"),
    path("add_teacher/",apis.TeacherApi().add_teacher,name="add_teacher"),

    path("majors/",views.MajorViews().majors,name="majors"),
    path("major/<int:pk>/",views.MajorViews().major,name="major"),
    path("add_major/",apis.MajorApi().add_major,name="add_major"),
    
    path("books/",views.BookViews().books,name="books"),
    path("book/<int:pk>/",views.BookViews().book,name="book"),
    
    path("session/<int:pk>/",views.SessionViews().session,name="session"),
    
    path("classrooms/",views.ClassRoomViews().classrooms,name="classrooms"),
    path("classroom/<int:pk>/",views.ClassRoomViews().classroom,name="classroom"),
    path("add_classroom/",apis.ClassRoomApi().add_classroom,name="add_classroom"),
    
    path("activecourse/<int:pk>/",views.CourseViews().active_course,name="activecourse"),
    path("course/<int:pk>/",views.CourseViews().course,name="course"),
]
