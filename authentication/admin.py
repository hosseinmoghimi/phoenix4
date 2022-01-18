from django.contrib import admin
from .models import MembershipRequest, Profile,ProfileContact

admin.site.register(MembershipRequest)
admin.site.register(Profile)
admin.site.register(ProfileContact)