from projectmanager.repo import OrganizationUnitRepo
from django import forms
from .apps import APP_NAME
from .models import Letter
from authentication.repo import ProfileRepo

class LetterRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Letter.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def letter(self, *args, **kwargs):
        if 'letter_id' in kwargs:
            return self.objects.filter(pk= kwargs['letter_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
            
    def add_letter(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_letter"):
            return
        letter=Letter()
        if 'title' in kwargs:
            letter.title= kwargs['title']
        if 'sender_id' in kwargs:
            letter.sender_id= kwargs['sender_id']
        else:
            letter.sender_id=OrganizationUnitRepo(request=self.request).objects.first().id
        
        if 'receiver_id' in kwargs:
            letter.receiver_id= kwargs['receiver_id']
        else:
            letter.receiver_id=OrganizationUnitRepo(request=self.request).objects.first().id
        letter.save()
        return letter