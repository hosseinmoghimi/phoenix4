from tinymce.models import HTMLField
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
from .enums import *
from django.shortcuts import reverse
IMAGE_FOLDER=APP_NAME+"/images/"

class Action(models.Model):
    game_role=models.ForeignKey("gamerole",related_name="action_doer_set", verbose_name=_("role1"), on_delete=models.CASCADE)
    action_target=models.ForeignKey("gamerole",related_name="action_target_set", verbose_name=_("role2"), on_delete=models.CASCADE)
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)
    night=models.IntegerField(_("night?"))
    role_block=models.BooleanField(_("role_block"),default=False)
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Event_detail", kwargs={"pk": self.pk})

class Game(models.Model):
    start_date=models.DateTimeField(_("start_date"), auto_now=False, auto_now_add=False)
    scenario=models.CharField(_("scenario"),choices=GameScenarioEnum.choices,max_length=50)
    god=models.ForeignKey("god",null=True,blank=True, verbose_name=_("god"), on_delete=models.CASCADE)

    def game_roles(self):
        return self.gamerole_set.all().order_by("turn")


    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")

    def __str__(self):
        return f"بازی شماره {self.id}"

    def get_absolute_url(self):
        return reverse(APP_NAME+":game", kwargs={"pk": self.pk})

class Player(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    score=models.IntegerField(_("score"),default=0)
    class_name="player"
    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")

    def __str__(self):
        return self.name
    @property
    def bio(self):
        return self.profile.bio if self.profile.bio is not None else ""
    @property
    def name(self):
        return self.profile.name
    @property
    def image(self):
        return self.profile.image
    def get_absolute_url(self):
        return reverse(APP_NAME+":player", kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_edit_btn(self):
        return f"""
                <a title="ویرایش" href="{self.get_edit_url()}">
                    <i class="material-icons">
                        edit
                    </i>
                </a>
        """
class God(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    score=models.IntegerField(_("score"),default=0)
    class Meta:
        verbose_name = _("God")
        verbose_name_plural = _("Gods")

    def __str__(self):
        return self.profile.name
    @property
    def name(self):
        return self.profile.name
    @property
    def image(self):
        return self.profile.image
    def get_absolute_url(self):
        return reverse(APP_NAME+":god", kwargs={"pk": self.pk})

class GameRole(models.Model):
    game=models.ForeignKey("Game", verbose_name=_("Game"), on_delete=models.CASCADE)
    role=models.ForeignKey("role", verbose_name=_("role"), on_delete=models.CASCADE)
    player=models.ForeignKey("player",null=True,blank=True, verbose_name=_("player"), on_delete=models.CASCADE)
    turn=models.IntegerField(_("نوبت"),default=20)
    description=models.CharField(_("description"),null=True,blank=True, max_length=50)
    class_name="gamerole"
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_edit_btn(self):
        return f"""
                <a title="ویرایش" href="{self.get_edit_url()}">
                    <i class="material-icons">
                        edit
                    </i>
                </a>
        """
    class Meta:
        verbose_name = _("GameRole")
        verbose_name_plural = _("GameRoles")

    def __str__(self):
        a=(("@ "+self.player.profile.name) if self.player is not None else "")
        return f"بازی شماره {self.game.id} {a} ({self.role})"

    def get_absolute_url(self):
        return reverse(APP_NAME+":game_role", kwargs={"game_role_id": self.pk})

class Role(models.Model):
    image_origin=models.ImageField(_("image"), upload_to=IMAGE_FOLDER+"role/",null=True,blank=True, height_field=None, width_field=None, max_length=None)
    priority=models.IntegerField(_("ترتیب"),default=100)
    side=models.CharField(_("side"),choices=SideEnums.choices, max_length=50)
    role_name=models.CharField(_("role"), max_length=50)
    default_count=models.IntegerField(_("default"),default=0)
    description=HTMLField(_("description"),null=True,blank=True)
    class_name="role"
    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.role_name
    def role_color(self):
        return "danger" if self.side==SideEnums.MAFIA else "success"
    def get_absolute_url(self):
        return reverse(APP_NAME+":role", kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_edit_btn(self):
        return f"""
                <a title="ویرایش" href="{self.get_edit_url()}">
                    <i class="material-icons">
                        edit
                    </i>
                </a>
        """
    @property
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        return STATIC_URL+APP_NAME+"/images/role.jpg"