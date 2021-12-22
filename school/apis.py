from django.http.response import JsonResponse
from school.forms import *
from school.repo import ClassRoomRepo, MajorRepo, SchoolRepo, SessionRepo, StudentRepo, TeacherRepo
from school.serializers import ClassRoomSerializer, MajorSerializer, SchoolSerializer, SessionSerializer, StudentSerializer, TeacherSerializer
from .apps import APP_NAME
from rest_framework.views import APIView
from core.constants import SUCCEED,FAILED
class SchoolApi(APIView):
    def add_school(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddSchoolForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                title=cd['title']
                school=SchoolRepo(request=request).add(title=title)
                if school is not None:
                    context['school']=SchoolSerializer(school).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class SessionApi(APIView):
    def add_session(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddSessionForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                active_course_id=cd['active_course_id']
                session=SessionRepo(request=request).add_session(active_course_id=active_course_id)
                if session is not None:
                    context['session']=SessionSerializer(session).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class TeacherApi(APIView):
    def add_teacher(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddTeacherForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                profile_id=cd['profile_id']
                teacher=TeacherRepo(request=request).add_teacher(profile_id=profile_id)
                if teacher is not None:
                    context['teacher']=TeacherSerializer(teacher).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class StudentApi(APIView):
    def add_student(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddStudentForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                profile_id=cd['profile_id']
                student=StudentRepo(request=request).add_student(profile_id=profile_id)
                if student is not None:
                    context['student']=StudentSerializer(student).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class ClassRoomApi(APIView):
    def add_classroom(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddClassRoomForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                title=cd['title']
                school_id=cd['school_id']
                classroom=ClassRoomRepo(request=request).add(title=title,school_id=school_id)
                if classroom is not None:
                    context['classroom']=ClassRoomSerializer(classroom).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class MajorApi(APIView):
    def add_major(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddMajorForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                title=cd['title']
                major=MajorRepo(request=request).add(title=title)
                if major is not None:
                    context['major']=MajorSerializer(major).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)