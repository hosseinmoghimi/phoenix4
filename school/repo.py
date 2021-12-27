from django.http import request
from authentication.repo import ProfileRepo
from core import repo as CoreRepo
import school
from school.enums import AttendanceStatusEnum
from .models import ActiveCourse, Attendance, ClassRoom, Course, Major, School, Session,Student,Teacher,Book
from .apps import APP_NAME
from django.db.models import Q
from django.utils import timezone


class AttendanceRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Attendance.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def attendance(self,*args, **kwargs):
        if 'attendance_id' in kwargs:
            return self.objects.filter(pk=kwargs['attendance_id']).first()
        elif 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        elif 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

    def add(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_attendance"):
            return
        now=timezone.now()
        session_id=kwargs['session_id'] if 'session_id' in kwargs else 0
        student_id=kwargs['student_id'] if 'student_id' in kwargs else 0
        description=kwargs['description'] if 'description' in kwargs else 0
        status=kwargs['status'] if 'status' in kwargs else AttendanceStatusEnum.NOT_SET

        session=SessionRepo(request=self.request).session(*args, **kwargs)
        student=StudentRepo(request=self.request).student(*args, **kwargs)

        if session is None or student is None:
            return
        enter_time=kwargs['enter_time'] if 'enter_time' in kwargs else session.start_time
        exit_time=kwargs['exit_time'] if 'exit_time' in kwargs else session.end_time

        attendance=Attendance()
        attendance.student=student
        attendance.session=session
        attendance.enter_time=enter_time
        attendance.exit_time=exit_time
        attendance.status=status
        attendance.description=description
        attendance.save()
        return attendance
class SchoolRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = School.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def school(self,*args, **kwargs):
        if 'school_id' in kwargs:
            pk=kwargs['school_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_school"):
            return
        school=School()
        if 'title' in kwargs:
            school.title=kwargs['title']
        school.save()
        return school

class MajorRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Major.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def major(self,*args, **kwargs):
        if 'major_id' in kwargs:
            pk=kwargs['major_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_major"):
            return
        major=Major()
        if 'title' in kwargs:
            major.title=kwargs['title']
        major.save()
        return major
    
class BookRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Book.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def book(self,*args, **kwargs):
        if 'book_id' in kwargs:
            pk=kwargs['book_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

class ClassRoomRepo():
   
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = ClassRoom.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def classroom(self,*args, **kwargs):
        if 'classroom_id' in kwargs:
            pk=kwargs['classroom_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_classroom"):
            return
        classroom=ClassRoom()
        if 'title' in kwargs:
            classroom.title=kwargs['title']
        if 'school_id' in kwargs:
            classroom.school_id=kwargs['school_id']
        classroom.save()
        return classroom

class ActiveCourseRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = ActiveCourse.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        return self.objects.all()
    
    def active_course(self,*args, **kwargs):
        if 'active_course_id' in kwargs:
            pk=kwargs['active_course_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()



class CourseRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Course.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    def course(self,*args, **kwargs):
        if 'course_id' in kwargs:
            pk=kwargs['course_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()




class SessionRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Session.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        return self.objects.all()
    def session(self,*args, **kwargs):
        if 'session_id' in kwargs:
            pk=kwargs['session_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_session(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_session"):
            return
        session=Session()
        if 'active_course_id' in kwargs:

            active_course_id=kwargs['active_course_id']
        else:
            return
        active_course=ActiveCourse.objects.filter(pk=active_course_id).first()
        if active_course is None:
            return

        session_no=1
        session.active_course_id=active_course_id
        if 'session_no' in kwargs:
            session_no=kwargs['session_no']
        else:
            session_1=Session.objects.filter(active_course_id=active_course_id).order_by('-session_no').first()
            if session_1 is not None:
                session_no=1+session_1.session_no

        session.session_no=session_no
        if 'title' in kwargs:
            session.title=kwargs['title']
        else:
            session.title="جلسه "+str(session_no)+" "+active_course.course.title
        
        if 'start_time' in kwargs:
            session.start_time=kwargs['start_time']
        else:
            session.start_time=timezone.now()
        
        if 'end_time' in kwargs:
            session.end_time=kwargs['end_time']
        else:
            session.end_time=timezone.now()

        session.save()
        return session

  

    
class TeacherRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Teacher.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(Q(profile__user__first_name__contains=kwargs['search_for'])|Q(profile__user__last_name__contains=kwargs['search_for']))
        return objects
    def teacher(self,*args, **kwargs):
        if 'profile_id' in kwargs:
            return self.objects.filter(profile_id=kwargs['profile_id']).first()
        if 'teacher_id' in kwargs:
            return self.objects.filter(pk=kwargs['teacher_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
         

    def add_teacher(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_teacher"):
            return

        teacher=self.teacher(*args, **kwargs)
        if teacher is None:
            teacher=Teacher()
            teacher.profile_id=kwargs['profile_id']
            teacher.save()
            return teacher


    
class StudentRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Student.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(Q(profile__user__first_name__contains=kwargs['search_for'])|Q(profile__user__last_name__contains=kwargs['search_for']))
        return objects
    def student(self,*args, **kwargs):
        if 'profile_id' in kwargs:
            return self.objects.filter(profile_id=kwargs['profile_id']).first()
        if 'student_id' in kwargs:
            pk=kwargs['student_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    

    def add_student(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_student"):
            return

        student=self.student(*args, **kwargs)
        if student is None:
            student=Student()
            student.profile_id=kwargs['profile_id']
            student.save()
            return student

