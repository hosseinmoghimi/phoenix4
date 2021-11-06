from django.db.models import fields
from .apps import APP_NAME
from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from .models import Book, ClassRoom, Course, Major, School, Student, Teacher

class StudentSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Student
        fields=['id','profile','get_absolute_url','get_edit_url']



class TeacherSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Teacher
        fields=['id','profile','get_absolute_url','get_edit_url']

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields=['id','title','get_absolute_url','get_edit_url']



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields=['id','title','get_absolute_url','get_edit_url']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields=['id','title','get_absolute_url','get_edit_url']


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields=['id','title','get_absolute_url','get_edit_url']

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields=['id','title','get_absolute_url','get_edit_url']
