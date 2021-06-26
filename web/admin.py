from django.contrib import admin

# Register your models here.
from .models import Award, ContactMessage, CountDownItem, FAQ, Feature, OurTeam, OurWork, ResumeCategory,Blog,Resume,Carousel, ResumeSkill, Technology, Testimonial

admin.site.register(ResumeCategory)
admin.site.register(ResumeSkill)
admin.site.register(Resume)
admin.site.register(Blog)
admin.site.register(Carousel)
admin.site.register(CountDownItem)
admin.site.register(Technology)
admin.site.register(Award)
admin.site.register(Feature)
admin.site.register(Testimonial)
admin.site.register(OurWork)
admin.site.register(OurTeam)
admin.site.register(ContactMessage)
admin.site.register(FAQ)









