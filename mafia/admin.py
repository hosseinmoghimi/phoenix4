from django.contrib import admin

# Register your models here.
from .models import Action, GameRole, God, Player,Game,Role

admin.site.register(Player)
admin.site.register(Action)
admin.site.register(Role)
admin.site.register(Game)
admin.site.register(GameRole)
admin.site.register(God)