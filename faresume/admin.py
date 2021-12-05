from django.contrib import admin

from faresume.models import Resume, ResumeCategory

# Register your models here.
admin.site.register(Resume)
admin.site.register(ResumeCategory)