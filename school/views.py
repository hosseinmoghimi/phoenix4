from django.shortcuts import render,reverse
from authentication.repo import ProfileRepo
from core.views import CoreContext, PageContext,ParametersEnum,ParameterRepo
from school.repo import ActiveCourseRepo, BookRepo, ClassRoomRepo, CourseRepo, MajorRepo, SchoolRepo, SessionRepo, StudentRepo, TeacherRepo
from school.serializers import MajorSerializer, CourseSerializer, BookSerializer, ClassRoomSerializer, SchoolSerializer, SessionSerializer, StudentSerializer, TeacherSerializer
from .apps import APP_NAME
from django.views import View
from .forms import *
import json
TEMPLATE_ROOT="school/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
    context['search_form']=SearchForm()
    
    context['search_action'] = reverse(APP_NAME+":search")
 
    return context

class BasicViews(View):
    def search(self, request, *args, **kwargs):
        context = getContext(request)
        log = 1
        if request.method == 'POST':
            log += 1
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                log += 1
                search_for = search_form.cleaned_data['search_for']
                context['search_for'] = search_for

                schools = SchoolRepo(request=request).list(search_for=search_for)
                context['schools'] =schools
                context['schools_s']=json.dumps(SchoolSerializer(schools,many=True).data)


                books = BookRepo(request=request).list(search_for=search_for)
                context['books'] = books
                context['books_s']=json.dumps(BookSerializer(books,many=True).data)


                teachers = TeacherRepo(request=request).list(search_for=search_for)
                context['teachers'] = teachers
                context['teachers_s']=json.dumps(TeacherSerializer(teachers,many=True).data)


                students = StudentRepo(request=request).list(search_for=search_for)
                context['students'] = students
                context['students_s']=json.dumps(StudentSerializer(students,many=True).data)
                

                classrooms = ClassRoomRepo(request=request).list(search_for=search_for)
                context['classrooms'] = classrooms
                context['classrooms_s']=json.dumps(ClassRoomSerializer(classrooms,many=True).data)


                courses = CourseRepo(request=request).list(search_for=search_for)
                context['courses'] = courses
                context['courses_s']=json.dumps(CourseSerializer(courses,many=True).data)


                 
                context['log'] = log
                return render(request, TEMPLATE_ROOT+"search.html", context)
        return BasicViews().home(request=request)

    def home(self,request,*args, **kwargs):
        context=getContext(request=request)


        schools=SchoolRepo(request=request).list(*args, **kwargs)
        context['schools']=schools
        context['schools_s']=json.dumps(SchoolSerializer(schools,many=True).data)


        classrooms=ClassRoomRepo(request=request).list(*args, **kwargs)
        context['classrooms']=classrooms
        context['classrooms_s']=json.dumps(ClassRoomSerializer(classrooms,many=True).data)


        majors=MajorRepo(request=request).list(*args, **kwargs)
        context['majors']=majors
        context['majors_s']=json.dumps(MajorSerializer(majors,many=True).data)




        teachers=TeacherRepo(request=request).list(*args, **kwargs)
        context['teachers']=teachers
        context['teachers_s']=json.dumps(TeacherSerializer(teachers,many=True).data)





        students=StudentRepo(request=request).list(*args, **kwargs)
        context['students']=students
        context['students_s']=json.dumps(StudentSerializer(students,many=True).data)




        books=BookRepo(request=request).list(*args, **kwargs)
        context['books']=books
        context['books_s']=json.dumps(BookSerializer(books,many=True).data)


        return render(request,TEMPLATE_ROOT+"index.html",context)


class ClassRoomViews(View):
    def classroom(self,request,*args, **kwargs):
        context=getContext(request=request)
        classroom=ClassRoomRepo(request=request).classroom(*args, **kwargs)
        context['classroom']=classroom
        return render(request,TEMPLATE_ROOT+"classroom.html",context)

    def classrooms(self,request,*args, **kwargs):
        context=getContext(request=request)
        classrooms=ClassRoomRepo(request=request).list(*args, **kwargs)
        context['classrooms']=classrooms
        context['classrooms_s']=json.dumps(ClassRoomSerializer(classrooms,many=True).data)
        return render(request,TEMPLATE_ROOT+"classrooms.html",context)


class SchoolViews(View):
    def school(self,request,*args, **kwargs):
        context=getContext(request=request)
        school=SchoolRepo(request=request).school(*args, **kwargs)
        context['school']=school
        classrooms=ClassRoomRepo(request=request).list(*args, **kwargs)
        context['classrooms']=classrooms
        context['classrooms_s']=json.dumps(ClassRoomSerializer(classrooms,many=True).data)

        if request.user.has_perm(APP_NAME+".add_classroom"):
            context['add_classroom_form']=AddClassRoomForm()


        return render(request,TEMPLATE_ROOT+"school.html",context)

    def schools(self,request,*args, **kwargs):
        context=getContext(request=request)
        schools=SchoolRepo(request=request).list(*args, **kwargs)
        context['schools_s']=json.dumps(SchoolSerializer(schools,many=True).data)

        if request.user.has_perm(APP_NAME+".add_school"):
            context['add_school_form']=AddSchoolForm()
        return render(request,TEMPLATE_ROOT+"schools.html",context)


        
class StudentViews(View):
    
    def student(self,request,*args, **kwargs):
        context=getContext(request=request)
        student=StudentRepo(request=request).student(*args, **kwargs)
        context['student']=student
        return render(request,TEMPLATE_ROOT+"student.html",context)

    def students(self,request,*args, **kwargs):
        context=getContext(request=request)
        students=StudentRepo(request=request).list(*args, **kwargs)
        context['students']=students
        context['students_s']=json.dumps(StudentSerializer(students,many=True).data)
        if request.user.has_perm(APP_NAME+".add_teacher"):
            context['add_student_form']=AddStudentForm()
            profiles=ProfileRepo(request=request).list()
            context['profiles']=profiles
        return render(request,TEMPLATE_ROOT+"students.html",context)
class CourseViews(View):
    def course(self,request,*args, **kwargs):
        context=getContext(request=request)
        course=CourseRepo(request=request).course(*args, **kwargs)
        context['course']=course
        context['books']=course.books.all()
        return render(request,TEMPLATE_ROOT+"course.html",context)


    def active_course(self,request,*args, **kwargs):
        context=getContext(request=request)
        active_course=ActiveCourseRepo(request=request).active_course(*args, **kwargs)
        context['books']=active_course.course.books.all()

        students=active_course.students.all()
        context['students']=students
        context['students_s']=json.dumps(StudentSerializer(students,many=True).data)


        sessions=active_course.session_set.all()
        context['sessions']=sessions
        context['sessions_s']=json.dumps(SessionSerializer(sessions,many=True).data)

        context['active_course']=active_course
        if request.user.has_perm(APP_NAME+".add_session"):
            context['add_session_form']=AddSessionForm()
        return render(request,TEMPLATE_ROOT+"active-course.html",context)


        
class TeacherViews(View):
    def teacher(self,request,*args, **kwargs):
        context=getContext(request=request)
        teacher=TeacherRepo(request=request).teacher(*args, **kwargs)
        context['teacher']=teacher
        return render(request,TEMPLATE_ROOT+"teacher.html",context)


    def teachers(self,request,*args, **kwargs):
        context=getContext(request=request)
        teachers=TeacherRepo(request=request).list(*args, **kwargs)
        context['teachers']=teachers
        context['teachers_s']=json.dumps(TeacherSerializer(teachers,many=True).data)
        if request.user.has_perm(APP_NAME+".add_teacher"):
            context['add_teacher_form']=AddTeacherForm()
            profiles=ProfileRepo(request=request).list()
            context['profiles']=profiles
        return render(request,TEMPLATE_ROOT+"teachers.html",context)


        
class MajorViews(View):
    def major(self,request,*args, **kwargs):
        context=getContext(request=request)
        major=MajorRepo(request=request).major(*args, **kwargs)
        context['major']=major
        return render(request,TEMPLATE_ROOT+"major.html",context)


    def majors(self,request,*args, **kwargs):
        context=getContext(request=request)
        majors=MajorRepo(request=request).list(*args, **kwargs)
        context['majors']=majors
        context['majors_s']=json.dumps(MajorSerializer(majors,many=True).data)


        if request.user.has_perm(APP_NAME+".add_major"):
            context['add_major_form']=AddMajorForm()

        return render(request,TEMPLATE_ROOT+"majors.html",context)


        
class BookViews(View):
    def book(self,request,*args, **kwargs):
        context=getContext(request=request)
        book=BookRepo(request=request).book(*args, **kwargs)
        context['book']=book
        return render(request,TEMPLATE_ROOT+"book.html",context)

    def books(self,request,*args, **kwargs):
        context=getContext(request=request)
        books=BookRepo(request=request).list(*args, **kwargs)
        context['books']=books
        return render(request,TEMPLATE_ROOT+"books.html",context)

        
class SessionViews(View):
    def session(self,request,*args, **kwargs):
        context=getContext(request=request)
        session=SessionRepo(request=request).session(*args, **kwargs)
        context.update(PageContext(request=request,page=session))
        context['session']=session
        context['course']=session.active_course.course

        students=session.active_course.students.all()
        context['students']=students
        context['students_s']=json.dumps(StudentSerializer(students,many=True).data)

        books=session.active_course.course.books.all()
        context['books']=books
        context['books_s']=json.dumps(BookSerializer(books,many=True).data)
        
        
        sessions=session.active_course.session_set.all()
        context['sessions']=sessions
        context['sessions_s']=json.dumps(SessionSerializer(sessions,many=True).data)
        return render(request,TEMPLATE_ROOT+"session.html",context)