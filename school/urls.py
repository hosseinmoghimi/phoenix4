from django.urls import path
from .apps import APP_NAME
from . import views,apis



from django.contrib.auth.decorators import login_required


app_name=APP_NAME
urlpatterns = [
    
    path("",login_required(views.BasicViews().home),name="home"),
    
    path("search/",login_required(views.BasicViews().search),name="search"),


    path("schools/",login_required(views.SchoolViews().schools),name="schools"),
    path("school/<int:school_id>/",login_required(views.SchoolViews().school),name="school"),
    path("api/add_school/",login_required(apis.SchoolApi().add_school),name="add_school"),

    path("students/",login_required(views.StudentViews().students),name="students"),
    path("student/<int:pk>/",login_required(views.StudentViews().student),name="student"),
    path("api/add_student/",login_required(apis.StudentApi().add_student),name="add_student"),

    path("teachers/",login_required(views.TeacherViews().teachers),name="teachers"),
    path("teacher/<int:pk>/",login_required(views.TeacherViews().teacher),name="teacher"),
    path("api/add_teacher/",login_required(apis.TeacherApi().add_teacher),name="add_teacher"),

    path("majors/",login_required(views.MajorViews().majors),name="majors"),
    path("major/<int:pk>/",login_required(views.MajorViews().major),name="major"),
    path("api/add_major/",login_required(apis.MajorApi().add_major),name="add_major"),
    
    path("books/",login_required(views.BookViews().books),name="books"),
    path("add_document/",login_required(apis.BookApi().add_document),name="add_document"),
    path("add_book/",login_required(apis.BookApi().add_book),name="add_book"),
    path("book/<int:pk>/",login_required(views.BookViews().book),name="book"),
    
    path("educationalyear/<int:pk>/",login_required(views.EducationalYearViews().educational_year),name="educationalyear"),
    
    path("session/<int:pk>/",login_required(views.SessionViews().session),name="session"),
    path("api/add_session/",login_required(apis.SessionApi().add_session),name="add_session"),
    path("api/add_attendance/",login_required(apis.AttendanceApi().add_attendance),name="add_attendance"),
    
    path("classrooms/",login_required(views.ClassRoomViews().classrooms),name="classrooms"),
    path("classroom/<int:pk>/",login_required(views.ClassRoomViews().classroom),name="classroom"),
    path("api/add_classroom/",login_required(apis.ClassRoomApi().add_classroom),name="add_classroom"),
    path("api/add_course/",login_required(apis.CourseApi().add_course),name="add_course"),
    path("api/add_active_course/",login_required(apis.ActiveCourseApi().add_active_course),name="add_active_course"),
    
    path('api/add_student_to_active_course/',login_required(apis.ActiveCourseApi().add_student_to_active_course),name="add_student_to_active_course"),
    path('api/add_teacher_to_active_course/',login_required(apis.ActiveCourseApi().add_teacher_to_active_course),name="add_teacher_to_active_course"),
    path("activecourses/",login_required(views.ActiveCourseViews().active_courses),name="active_courses"),
    path("activecourse/<int:pk>/",login_required(views.ActiveCourseViews().active_course),name="activecourse"),
    path("course/<int:pk>/",login_required(views.CourseViews().course),name="course"),
    path("courses/",login_required(views.CourseViews().courses),name="courses"),
]
