from core.repo import ParameterRepo
from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, Http404
from .apps import APP_NAME
from .repo import *
from django.views import View
from .serializers import *
from .enums import *
from .constants import *
from .forms import *
from core.views import CoreContext, MessageView
TEMPLATE_ROOT = 'bms/'


def getContext(request):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['layout_parent']="material-dashboard-5-rtl/layout.html"
    context['layout_parent']="phoenix/layout.html"
    return context


class BasicViews(View):
    def logs(self, request, *args, **kwargs):
        context = getContext(request)
        user = request.user
        per_page = CoreRepo.ParameterRepo(app_name=APP_NAME,user=request.user).get(name=ParameterEnums.LOG_PER_PAGE)
        try:
            a=int(per_page)
        except:
            per_page=10
        context['per_page'] = per_page
        logs = LogRepo(user=user).list().order_by('-id')[0:per_page]
        context['logs'] = logs
        context['get_log_form'] = GetLogForm()
        return render(request, TEMPLATE_ROOT+"logs.html", context)

    def home(self, request, *args, **kwargs):
        context = getContext(request)
        user = request.user
        me = CoreRepo.ProfileRepo(user=user).me
        if me is not None:
            # scenarioes=ScenarioRepo(user=user).list()
            scenarioes = me.scenario_set.all()
            context['scenarioes'] = scenarioes
        feeders = FeederRepo(user=user).list()
        context['feeders'] = feeders
        context['relays'] = [1, 2, 3, 4]
        return render(request, TEMPLATE_ROOT+"index.html", context)


    def scenario(self, request, pk, *args, **kwargs):
        context = getContext(request)
        user = request.user
        me = CoreRepo.ProfileRepo(user=user).me
        if me is not None:
            scenario = ScenarioRepo(user=user).scenario(pk=pk)
            context['scenario'] = scenario
        return render(request, TEMPLATE_ROOT+"scenario.html", context)

    def feeder(self, request, *args, **kwargs):
        context = getContext(request=request)
        user = request.user
        me = CoreRepo.ProfileRepo(user=user).me
        if me is not None:
            feeder_repo=FeederRepo(user=user)
            feeder = feeder_repo.feeder(*args, **kwargs)
            if feeder is None:
                mv=MessageView(request=request)
                mv.header_text="no feeder"
                mv.message_text="feeder not found"
                return mv.show()
            (regs,feeder)=feeder_repo.get_state(feeder=feeder)
            context['feeder'] = feeder
            # return JsonResponse(str(a),safe=False)
            commands = CommandRepo(request=request).my_commands(feeder=feeder)
            context['commands'] = commands

        return render(request, TEMPLATE_ROOT+"feeder.html", context)

    def command(self, request, pk, *args, **kwargs):
        command = CommandRepo(request=request).command(pk)
        if command is None:
            raise Http404
        context = getContext(request)
        context['command'] = command
        logs = LogRepo(request=request).list().filter(command=command).order_by('-id')[:100]
        context['logs'] = logs
        return render(request, TEMPLATE_ROOT+"command.html", context)

    def relay(self, request, pk, *args, **kwargs):
        relay = RelayRepo(request=request).relay(pk)
        if relay is None:
            raise Http404

        context = getContext(request)
        context['relay'] = relay
        logs = LogRepo(request=request).list().filter(relay=relay).order_by('-id')[:100]
        context['logs'] = logs
        return render(request, TEMPLATE_ROOT+"relay.html", context)
