from datetime import datetime
import math
from django.db.models.base import Model
from tinymce.models import HTMLField
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
from .enums import *
from utility.num import to_tartib
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
    status=models.CharField(_("وضعیت بازی"),choices=GameStatusEnums.choices, max_length=50)
    def current_day(self):
        if self.status==GameStatusEnums.DAY_IN_PROGRESS:
            return GameDay.objects.filter(game=self).order_by("-counter").first()
        if self.status==GameStatusEnums.COURT_VOTING:
            return GameDay.objects.filter(game=self).order_by("-counter").first()
        if self.status==GameStatusEnums.ACCUSE_VOTING:
            return GameDay.objects.filter(game=self).order_by("-counter").first()

    class_name="game"
    def next_state(self):
        state=GameStatusEnums.CREATING
        if self.status==GameStatusEnums.CREATING:
            state=GameStatusEnums.ROLING
        if self.status==GameStatusEnums.ROLING:
            state=GameStatusEnums.INTRODUCING
        if self.status==GameStatusEnums.INTRODUCING:
            state=GameStatusEnums.DAY_IN_PROGRESS
        if self.status==GameStatusEnums.DAY_IN_PROGRESS:
            state=GameStatusEnums.COURT_VOTING
        if self.status==GameStatusEnums.COURT_VOTING:
            state=GameStatusEnums.ACCUSE_VOTING
        if self.status==GameStatusEnums.ACCUSE_VOTING:
            state=GameStatusEnums.NIGHT_IN_PROGRESS
        if self.status==GameStatusEnums.NIGHT_IN_PROGRESS:
            state=GameStatusEnums.DAY_IN_PROGRESS
        return state
    def votes_to_act(self):
        n=len(self.live_gameroles())
        n=n/2
        n=math.floor(n)
        return n
    def next_night_no(self):
        return len(GameNight.objects.filter(game=self))+1
    def next_day_no(self):
        return len(GameDay.objects.filter(game=self))+1
    def live_gameroles(self):
        return self.gamerole_set.filter(status=GameRoleStateEnum.ALIVE)
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    
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
    status=models.CharField(_("state"),choices=GameRoleStateEnum.choices,default=GameRoleStateEnum.ALIVE, max_length=50)
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
        verbose_name_plural = _("نقش های بازی")
    @property
    def name(self):
        if self.player is not None:
            return self.player.profile.name
        else:
            return self.role.role_name
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
    night_act_title=models.CharField(_("عنوان اکت شب"),null=True,blank=True, max_length=50)
    night_act_max=models.IntegerField(_("تعداد اکت شب"),default=0)
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

class GameNight(models.Model):
    game=models.ForeignKey("game", verbose_name=_("بازی"), on_delete=models.CASCADE)
    counter=models.IntegerField(_("شماره شب"))
    status=models.CharField(_("وضعیت"),choices=GameDayNightStatusEnum.choices, max_length=50)


    

    class Meta:
        verbose_name = _("GameNight")
        verbose_name_plural = _("شب های بازی")

    def __str__(self):
        return f'شب {to_tartib(self.counter)}  از  {str(self.game)}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":game_night", kwargs={"pk": self.pk})

class GameDay(models.Model):
    game=models.ForeignKey("game", verbose_name=_("بازی"), on_delete=models.CASCADE)
    counter=models.IntegerField(_("شماره روز"))
    status=models.CharField(_("status"),choices=GameDayNightStatusEnum.choices, max_length=50)

    
    def title(self):
        return f'روز {to_tartib(self.counter)}  از  {str(self.game)}'
    class Meta:
        verbose_name = _("GameDay")
        verbose_name_plural = _("روزهای بازی")


    def __str__(self):
        return f'روز {to_tartib(self.counter)}  از  {str(self.game)}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":game_day", kwargs={"pk": self.pk})

class NightAct(models.Model):
    title=models.CharField(_("title"), max_length=100)
    # act=models.CharField(_("act"),choices=NightActEnum.choices, max_length=50)
    night=models.ForeignKey("gamenight", verbose_name=_("gamenight"), on_delete=models.CASCADE)
    actor_role=models.ForeignKey("gamerole",related_name="night_actor_set", verbose_name=_("نقش فاعل"), on_delete=models.CASCADE)
    acted_role=models.ForeignKey("gamerole",related_name="night_acted_set", verbose_name=_("نقش"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    class Meta:
        verbose_name = _("NightShot")
        verbose_name_plural = _("شات های شب")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("NightShot_detail", kwargs={"pk": self.pk})

class Vote(models.Model):
    day=models.ForeignKey("gameday", verbose_name=_("روز بازی"), on_delete=models.CASCADE)
    voter=models.ForeignKey("gamerole",null=True,blank=True,related_name="voter_set", verbose_name=_("رای دهنده"), on_delete=models.CASCADE)
    accused=models.ForeignKey("gamerole",related_name="voteaccused_set", verbose_name=_("متهم"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    level=models.CharField(_("مرحله"), choices=VoteLevelEnum.choices,default=VoteLevelEnum.COURT,max_length=50)
    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")

    def __str__(self):
        voter="" if self.voter is None else self.voter.player.profile.name
        return f"رای {voter} به {self.accused.name} در {str(self.day)} ({self.level})"

    def get_absolute_url(self):
        return reverse("Vote_detail", kwargs={"pk": self.pk})

class Accused(models.Model):
    day=models.ForeignKey("gameday", verbose_name=_("روز بازی"), on_delete=models.CASCADE)
    game_role=models.ForeignKey("GameRole", verbose_name=_("بازیکن"), on_delete=models.CASCADE)
    votes_count=models.IntegerField(_("تعداد رای های خروج"))
    class Meta:
        verbose_name = _("Accused")
        verbose_name_plural = _("Accuseds")

    def __str__(self):
        return f"{self.game_role.player.profile.name} @ {str(self.day.game)}"

    def get_absolute_url(self):
        return reverse("accused", kwargs={"pk": self.pk})
