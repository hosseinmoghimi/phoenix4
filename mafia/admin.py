from django.contrib import admin

# Register your models here.
from .models import God, Player,Game

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(God)