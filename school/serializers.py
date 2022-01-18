
from core.serializers import DocumentSerializer, PageLinkSerializer
from school.repo import EducationalYearRepo
from .apps import APP_NAME
from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from .models import ActiveCourse, Attendance, Book, ClassRoom, Course, EducationalYear, Major, School, Session, Student, Teacher

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



class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields=['id','title','get_absolute_url','get_edit_url']

class EducationalYearSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationalYear
        fields=['id','title','get_absolute_url']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields=['id','title','level','course_count','get_absolute_url','get_edit_url']

class CourseSerializerWithMajors(serializers.ModelSerializer):
    majors=MajorSerializer(many=True)
    class Meta:
        model = Course
        fields=['id','title','level','course_count','majors','get_absolute_url','get_edit_url']


class ActiveCourseSerializer(serializers.ModelSerializer):
    classroom=ClassRoomSerializer()
    year=EducationalYearSerializer()
    course=CourseSerializer()
    class Meta:
        model = ActiveCourse
        fields=['id','title','course','year','classroom','get_absolute_url','get_edit_url']

class AttendanceSerializer(serializers.ModelSerializer):
    session=SessionSerializer()
    student=StudentSerializer()
    class Meta:
        model = Attendance
        fields=['id','session','status','color','student','get_delete_url','description','persian_time_added','persian_enter_time','persian_exit_time','get_edit_url']



class BookSerializer(serializers.ModelSerializer):
    links=PageLinkSerializer(many=True)
    documents=DocumentSerializer(many=True)
    courses=CourseSerializer(many=True)
    class Meta:
        model = Book
        fields=['id','title','courses','get_absolute_url','get_edit_url','documents','links','get_delete_url']

