from django.contrib import admin

# Register your models here.
from .models import Action, GameDay, GameNight, GameRole, God, Player,Game,Role, Vote

admin.site.register(Player)
admin.site.register(Action)
admin.site.register(Role)
admin.site.register(Game)
admin.site.register(GameRole)
admin.site.register(God)
admin.site.register(GameNight)
admin.site.register(GameDay)
admin.site.register(Vote)