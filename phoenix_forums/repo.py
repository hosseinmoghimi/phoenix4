from phoenix_forums.models import Forum, Post
from core import repo as CoreRepo

class ForumRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Forum.objects
    def forum(self, *args, **kwargs):
        pk=0
        if 'forum_id' in kwargs:
            pk=kwargs['forum_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])

        return objects

class PostRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Post.objects
    
    def post(self, *args, **kwargs):
        pk=0
        if 'post_id' in kwargs:
            pk=kwargs['post_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])

        return objects