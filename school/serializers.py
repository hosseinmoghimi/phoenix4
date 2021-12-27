from django.db.models import fields
from .apps import APP_NAME
from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from .models import ActiveCourse, Attendance, Book, ClassRoom, Course, Major, School, Session, Student, Teacher

class StudentSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Student
        fields=['id','profile','get_absolute_url','get_edit_url']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields=['id','title','session_no','get_edit_url','get_absolute_url']


class TeacherSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Teacher
        fields=['id','profile','get_absolute_url','get_edit_url']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields=['id','title','get_absolute_url','get_edit_url']

class ClassRoomSerializer(serializers.ModelSerializer):
    school=SchoolSerializer()
    class Meta:
        model = ClassRoom
        fields=['id','title','school','get_absolute_url','get_edit_url']



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields=['id','title','get_absolute_url','get_edit_url']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields=['id','title','level','course_count','get_absolute_url','get_edit_url']


class ActiveCourseSerializer(serializers.ModelSerializer):
    classroom=ClassRoomSerializer()
    class Meta:
        model = ActiveCourse
        fields=['id','title','classroom','get_absolute_url','get_edit_url']


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields=['id','title','get_absolute_url','get_edit_url']

class AttendanceSerializer(serializers.ModelSerializer):
    session=SessionSerializer()
    student=StudentSerializer()
    class Meta:
        model = Attendance
        fields=['id','session','status','student','description','persian_time_added','persian_enter_time','persian_exit_time','get_edit_url']



