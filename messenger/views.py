from authentication.repo import ProfileRepo
from .serializers import MemberSerializer
from .repo import MemberRepo, MessageRepo,ChannelRepo
from django.shortcuts import render
from .apps import APP_NAME
from django.views import View
from core.views import CoreContext
import json
from messenger import apps
TEMPLATE_ROOT=APP_NAME+"/"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context



class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        channels=ChannelRepo(request=request).list(*args, **kwargs)
        context['channels']=channels

        
        # events=EventRepo(request=request).list(for_home=True,*args, **kwargs)
        # context['events']=events

        
        return render(request,TEMPLATE_ROOT+"index.html",context)
class MessageViews(View):
    def message(self,request,*args, **kwargs):
        context=getContext(request=request)
        message=MessageRepo(request=request).message(*args, **kwargs)
        context['message']=message
        return render(request,TEMPLATE_ROOT+"message.html",context)

def GetMemberContext(request):
    context={}
    profile=ProfileRepo(request=request).me
    
    member=profile.member_set.first()
    if member is not None:
        context['member']=member
        context['member_s']=json.dumps(MemberSerializer(member).data)
        channels=[]
        context['channels']=channels
    return context

class ChannelViews(View):
    def channel(self,request,*args, **kwargs):
        context=getContext(request=request)
        channel=ChannelRepo(request=request).channel(*args, **kwargs)
        context['channel']=channel
        messages=MessageRepo(request=request).list(channel_id=channel.id,*args, **kwargs).order_by("-id")
        context['messages']=messages
        context.update(GetMemberContext(request=request))
        members=channel.member_set.all()
        context['members']=members
        return render(request,TEMPLATE_ROOT+"channel.html",context)

    def member(self,request,*args, **kwargs):
        context=getContext(request=request)
        member=MemberRepo(request=request).member(*args, **kwargs)
        context['member']=member
        return render(request,TEMPLATE_ROOT+"member.html",context)

  
# class EventViews(View):
#     def event(self,request,*args, **kwargs):
#         context=getContext(request=request)
#         event=EventRepo(request=request).event(*args, **kwargs)
#         context['event']=event
#         return render(request,TEMPLATE_ROOT+"event.html",context)

  