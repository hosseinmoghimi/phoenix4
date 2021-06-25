from django.contrib import admin

# Register your models here.
from .models import ResumeCategory,Blog,Resume,Carousel

admin.site.register(ResumeCategory)
admin.site.register(Resume)
admin.site.register(Blog)
admin.site.register(Carousel)