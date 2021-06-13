from django.db.models.query_utils import Q
from authentication.repo import ProfileRepo
from messenger.models import Message


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