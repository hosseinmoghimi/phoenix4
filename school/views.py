from django.shortcuts import render
from core.views import CoreContext
from school.repo import ActiveCourseRepo, BookRepo, ClassRoomRepo, CourseRepo, SchoolRepo, SessionRepo, StudentRepo, TeacherRepo
from .apps import APP_NAME
from django.views import View

TEMPLATE_FOLDER="school/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        schools=SchoolRepo(request=request).list(*args, **kwargs)
        context['schools']=schools

        classrooms=ClassRoomRepo(request=request).list(*args, **kwargs)
        context['classrooms']=classrooms




        teachers=TeacherRepo(request=request).list(*args, **kwargs)
        context['teachers']=teachers




        students=StudentRepo(request=request).list(*args, **kwargs)
        context['students']=students




        books=BookRepo(request=request).list(*args, **kwargs)
        context['books']=books

        return render(request,TEMPLATE_FOLDER+"index.html",context)


class SchoolViews(View):
    def school(self,request,*args, **kwargs):
        context=getContext(request=request)
        school=SchoolRepo(request=request).school(*args, **kwargs)
        context['school']=school
        return render(request,TEMPLATE_FOLDER+"school.html",context)

    def classroom(self,request,*args, **kwargs):
        context=getContext(request=request)
        classroom=ClassRoomRepo(request=request).classroom(*args, **kwargs)
        context['classroom']=classroom
        return render(request,TEMPLATE_FOLDER+"classroom.html",context)


        
class StudentViews(View):
    def student(self,request,*args, **kwargs):
        context=getContext(request=request)
        student=StudentRepo(request=request).student(*args, **kwargs)
        context['student']=student
        return render(request,TEMPLATE_FOLDER+"student.html",context)


        
        
class CourseViews(View):
    def course(self,request,*args, **kwargs):
        context=getContext(request=request)
        course=CourseRepo(request=request).course(*args, **kwargs)
        context['course']=course
        return render(request,TEMPLATE_FOLDER+"course.html",context)


    def active_course(self,request,*args, **kwargs):
        context=getContext(request=request)
        active_course=ActiveCourseRepo(request=request).active_course(*args, **kwargs)
        context['active_course']=active_course
        return render(request,TEMPLATE_FOLDER+"active-course.html",context)


        
class TeacherViews(View):
    def teacher(self,request,*args, **kwargs):
        context=getContext(request=request)
        teacher=TeacherRepo(request=request).teacher(*args, **kwargs)
        context['teacher']=teacher
        return render(request,TEMPLATE_FOLDER+"teacher.html",context)


        
class BookViews(View):
    def book(self,request,*args, **kwargs):
        context=getContext(request=request)
        book=BookRepo(request=request).book(*args, **kwargs)
        context['book']=book
        return render(request,TEMPLATE_FOLDER+"book.html",context)

        
class SessionViews(View):
    def session(self,request,*args, **kwargs):
        context=getContext(request=request)
        session=SessionRepo(request=request).session(*args, **kwargs)
        context['session']=session
        return render(request,TEMPLATE_FOLDER+"session.html",context)