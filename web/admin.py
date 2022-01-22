from django.contrib import admin

# Register your models here.
from .models import Award,CryptoToken, ContactMessage, CountDownItem, FAQ, Feature, OurTeam, OurWork, Blog,Carousel, Technology, Testimonial

admin.site.register(Blog)
admin.site.register(CryptoToken)
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









