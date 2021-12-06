from authentication.repo import ProfileRepo
from core import repo as CoreRepo
import school
from .models import ActiveCourse, ClassRoom, Course, Major, School, Session,Student,Teacher,Book
from .apps import APP_NAME
from django.db.models import Q

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
        if 'teacher_id' in kwargs:
            pk=kwargs['teacher_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()




    
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
        if 'student_id' in kwargs:
            pk=kwargs['student_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()