import pusher
from django.db.models.query_utils import Q
from pusher.http import request_method
from authentication.repo import ProfileRepo
from messenger.models import Message,Channel,Event


class MessageRepo:
    def __init__(self,*args, **kwargs):        
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Message.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(Q(draft=True)|Q(read=False))
        return objects
    def message(self,*args, **kwargs):
        if 'message_id' in kwargs:
            pk=kwargs['message_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def send_message(self,message_text,channel_id,event):
        channel=ChannelRepo(request=self.request).channel(channel_id=channel_id)
        if channel is None:
            return
        pusher_client = pusher.Pusher(
            app_id=channel.app_id,
            key=channel.key,
            secret=channel.secret,
            cluster=channel.cluster,
            ssl=True
            )
        message_body={'message':message_text}
        pusher_client.trigger(channel.name, event, message_body)
        return None

class EventRepo:
    def __init__(self,*args, **kwargs):        
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Event.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'for_home' in kwargs:
            objects=objects
        return objects.all()
    def event(self,*args, **kwargs):
        if 'event_id' in kwargs:
            pk=kwargs['event_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()



class ChannelRepo:
    def __init__(self,*args, **kwargs):        
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Channel.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'for_home' in kwargs:
            objects=objects
        return objects.all()
    def channel(self,*args, **kwargs):
        if 'channel_id' in kwargs:
            pk=kwargs['channel_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()



class MemberRepo:
    def __init__(self,*args, **kwargs):        
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Member.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'for_home' in kwargs:
            objects=objects
        return objects.all()
    def member(self,*args, **kwargs):
        if 'member_id' in kwargs:
            pk=kwargs['member_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()


