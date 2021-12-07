from django.contrib import admin

from school.models import ActiveCourse, Attendance, Book, ClassRoom, Course, EducationalYear, Major, School, Session, Student, Teacher
admin.site.register(School)
admin.site.register(Attendance)
admin.site.register(Session)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(EducationalYear)
admin.site.register(ClassRoom)
admin.site.register(Book)
admin.site.register(Course)
admin.site.register(Major)
admin.site.register(ActiveCourse)
# Register your models here.
