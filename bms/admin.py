from django.contrib import admin
from .models import Feeder,Relay,Command,Scenario,Log

admin.site.register(Feeder)

admin.site.register(Relay)
admin.site.register(Command)
admin.site.register(Log)
admin.site.register(Scenario)