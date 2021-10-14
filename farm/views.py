import json
from .utils import AdminUtility
from django.shortcuts import render
from django.views import View
from .apps import APP_NAME
from .repo import *
from .enums import *
from .forms import *
from .serializers import *
from core.enums import ParametersEnum, MainPicEnum
# from web.repo import NavBarLinkRepo
from core.views import CoreContext,ParameterRepo

TEMPLATE_ROOT = APP_NAME+"/"

# TEMPLATE_ROOT = "material-dashboard-5/"

def getContext(request):
    context = CoreContext(request=request, app_name=APP_NAME)
    user = request.user
    context['admin_farm'] = AdminUtility(app_name=APP_NAME, user=request.user)
    parameter_repo = CoreRepo.ParameterRepo(
        user=request.user, app_name=APP_NAME)
    picture_repo = CoreRepo.PictureRepo(user=request.user, app_name=APP_NAME)
    link_repo = CoreRepo.LinkRepo(user=request.user)
    context['search_action'] = reverse(APP_NAME+":search")
    context['search_form'] = SearchForm()
    # navbar_links_repo = NavBarLinkRepo()
    # # navbar_links = navbar_links_repo.list_roots(app_name=APP_NAME)
    # navbar_buttons = navbar_links_repo.buttons(app_name=APP_NAME)
    context['app'] = {
        # 'navbar_links': navbar_links,
        # 'navbar_buttons': navbar_buttons,
        # 'social_links': CoreRepo.SocialLinkRepo(user=user).list_for_app(app_name=APP_NAME),
        # 'our_team_title': CoreRepo.OurTeamRepo(user=user, app_name=APP_NAME).get_title(),
        # 'our_team_link': CoreRepo.OurTeamRepo(user=user, app_name=APP_NAME).get_link(),
    }
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
    context['app'] = {
        'home_url': reverse(APP_NAME+":home"),
        'tel': parameter_repo.get(ParametersEnum.TEL).value,
        'title': parameter_repo.get(ParametersEnum.TITLE).value,
        'theme_color': parameter_repo.get(ParametersEnum.THEME_COLOR),
        'about_us_short': parameter_repo.get(ParametersEnum.ABOUT_US_SHORT),
        'NAV_TEXT_COLOR': parameter_repo.get(ParametersEnum.NAV_TEXT_COLOR),
        'NAV_BACK_COLOR': parameter_repo.get(ParametersEnum.NAV_BACK_COLOR),
        'slogan': parameter_repo.get(ParametersEnum.SLOGAN),
        'logo': picture_repo.get(name=MainPicEnum.LOGO),
        'favicon': picture_repo.get(name=MainPicEnum.FAVICON),
        'loading': picture_repo.get(name=MainPicEnum.LOADING),
        'pretitle': parameter_repo.get(ParametersEnum.PRE_TILTE),
        'address': parameter_repo.get(ParametersEnum.ADDRESS),
        'mobile': parameter_repo.get(ParametersEnum.MOBILE),
        'email': parameter_repo.get(ParametersEnum.EMAIL),
        'tel': parameter_repo.get(ParametersEnum.TEL),
    }
    context['APP_NAME'] = APP_NAME
    return context


class BasicViews(View):
    def home(self, request, *args, **kwargs):

        context = getContext(request)

        context['categories']=(i[0] for i in AnimalCategoryEnum.choices)

        animals = AnimalRepo(request=request).list()
        context['animals'] = animals

        saloons = SaloonRepo(request=request).list()
        context['saloons'] = saloons

        drugs = DrugRepo(request=request).list()
        context['drugs'] = drugs

        farms = FarmRepo(request=request).list()
        context['farms'] = farms

        doctors = DoctorRepo(request=request).list()
        context['doctors'] = doctors

        saloons = SaloonRepo(request=request).list()
        context['saloons'] = saloons

        return render(request, TEMPLATE_ROOT+"index.html", context)

    def drug(self, request, pk, *args, **kwargs):

        context = getContext(request)
        drug = DrugRepo(request=request).drug(pk)
        context['drug'] = drug
        return render(request, TEMPLATE_ROOT+"drug.html", context)

    def koshtar(self, request, *args, **kwargs):

        context = getContext(request)
        koshtar = KoshtarRepo(request=request).koshtar(*args, **kwargs)
        context['koshtar'] = koshtar
        return render(request, TEMPLATE_ROOT+"koshtar.html", context)

    def search(self, request, *args, **kwargs):
        context = getContext(request)
        log = 1
        if request.method == 'POST':
            log += 1
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                log += 1
                search_for = search_form.cleaned_data['search_for']
                context['search_for'] = search_for
                context['animals'] = AnimalRepo(request=request).list(search_for=search_for)
                context['saloons'] = SaloonRepo(request=request).list(search_for=search_for)
                context['log'] = log
                return render(request, TEMPLATE_ROOT+"search.html", context)

    def saloon(self, request, *args, **kwargs):

        context = getContext(request)
        saloon = SaloonRepo(request=request).saloon(*args, **kwargs)
        context['saloon'] = saloon
        costs=saloon.cost_set.all()
        context['costs'] = costs
        context['cost_categories']=(i[0] for i in CostCategoryEnum.choices)
        return render(request, TEMPLATE_ROOT+"saloon.html", context)

    def farm(self, request, pk, *args, **kwargs):

        context = getContext(request)
        farm = FarmRepo(request=request).farm(pk)
        context['farm'] = farm
        return render(request, TEMPLATE_ROOT+"farm.html", context)

    def doctor(self, request, pk, *args, **kwargs):

        context = getContext(request)
        doctor = DoctorRepo(request=request).doctor(pk)
        context['doctor'] = doctor
        return render(request, TEMPLATE_ROOT+"doctor.html", context)

    def employee(self, request, *args, **kwargs):

        context = getContext(request)
        employee = EmployeeRepo(request=request).employee(*args, **kwargs)
        context['employee'] = employee
        return render(request, TEMPLATE_ROOT+"employee.html", context)

    def food(self, request, pk, *args, **kwargs):
        context = getContext(request)
        food = FoodRepo(request=request).food(pk)
        context['food'] = food
        return render(request, TEMPLATE_ROOT+"food.html", context)

    def animal(self, request, *args, **kwargs):
        context = getContext(request)
        animal_repo = AnimalRepo(request=request)
        animal = animal_repo.animal(*args, **kwargs)
        context['animal'] = animal
        saloons = SaloonRepo(user=request.user).list()
        context['saloons'] = saloons
        ll=AnimalInSaloon.objects.filter(animal=animal).order_by('enter_date')[:10]
        weights=[0]
        max_weight=0
        for lll in list(ll):
            weights.append(lll.animal_weight)
            if max_weight<lll.animal_weight:
                max_weight=lll.animal_weight
        context['weights']=json.dumps(weights)
        context['max_weight']=max_weight
        context['animalinsaloon_set'] = animal.animalinsaloon_set.order_by(
            '-enter_date')
        context['saloon_foods'] = animal.foods()
        return render(request, TEMPLATE_ROOT+"animal.html", context)

    def saloonfood(self, request, pk, *args, **kwargs):
        context = getContext(request)
        saloon_food = SaloonFoodRepo(request=request).saloon_food(pk=pk)
        context['saloon_food'] = saloon_food
        return render(request, TEMPLATE_ROOT+"saloon-food.html", context)

    def animals(self, request, *args, **kwargs):
        context = getContext(request)
        animals = AnimalRepo(request=request).list(*args, **kwargs)
        context['animals'] = animals
        return render(request, TEMPLATE_ROOT+"animals.html", context)
class CostViews(View):
    def cost(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['cost']=CostRepo(request=request).cost(*args, **kwargs)
        return render(request,TEMPLATE_ROOT+"cost.html",context)