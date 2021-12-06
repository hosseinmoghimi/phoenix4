from django.http.response import JsonResponse
from school.forms import *
from school.repo import ClassRoomRepo, MajorRepo, SchoolRepo
from school.serializers import ClassRoomSerializer, MajorSerializer, SchoolSerializer
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