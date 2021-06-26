from django.contrib import admin
from .models import ResumeIndex, ResumePortfolio, ResumeService, ResumeSkill,Resume,ResumeCategory, ResumeTestimonial
# Register your models here.

admin.site.register(ResumeCategory)
admin.site.register(ResumeSkill)
admin.site.register(Resume)
admin.site.register(ResumeIndex)
admin.site.register(ResumePortfolio)
admin.site.register(ResumeService)
admin.site.register(ResumeTestimonial)



