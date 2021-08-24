from messenger.serializers import MessageSerializer
from authentication.serializers import ProfileSerializer
import pusher
from django.db.models.query_utils import Q
from pusher.http import request_method
from authentication.repo import ProfileRepo
from messenger.models import Message,Channel


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
        if 'channel_id' in kwargs:
            objects=objects.filter(channel_id=kwargs['channel_id'])
        if 'for_home' in kwargs:
            objects=objects.all()
        return objects
    def message(self,*args, **kwargs):
        if 'message_id' in kwargs:
            pk=kwargs['message_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def send_message(self,message_title,message_body,channel_id,event):
        channel=ChannelRepo(request=self.request).channel(channel_id=channel_id)
        
        message=Message()
        message.channel=channel
        message.event=event
        message.title=message_title
        message.body=message_body
        message.sender=ProfileRepo(request=self.request).me
        message.save()
        
        if channel is None:
            return
        pusher_client = pusher.Pusher(
            app_id=channel.app_id,
            key=channel.key,
            secret=channel.secret,
            cluster=channel.cluster,
            ssl=True
            )
        import json
        sender=(ProfileSerializer(message.sender).data)
        # message_object={'sender':sender,'title':message.title,'body':message.body}
        message_object=MessageSerializer(message).data
        pusher_client.trigger(channel.name, event, message_object)
        return message

# class EventRepo:
#     def __init__(self,*args, **kwargs):        
#         self.request = None
#         self.user = None
#         if 'request' in kwargs:
#             self.request = kwargs['request']
#             self.user = self.request.user
#         if 'user' in kwargs:
#             self.user = kwargs['user']
#         self.objects = Event.objects
#         self.me=ProfileRepo(user=self.user).me
#     def list(self,*args, **kwargs):
#         objects=self.objects.all()
#         if 'for_home' in kwargs:
#             objects=objects
#         return objects.all()
#     def event(self,*args, **kwargs):
#         if 'event_id' in kwargs:
#             pk=kwargs['event_id']
#         if 'pk' in kwargs:
#             pk=kwargs['pk']
#         if 'id' in kwargs:
#             pk=kwargs['id']
#         return self.objects.filter(pk=pk).first()



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


