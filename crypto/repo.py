from django import forms
from .apps import APP_NAME
from .models import CryptoToken
from authentication.repo import ProfileRepo

class CryptoTokenRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = CryptoToken.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def crypto_token(self, *args, **kwargs):
        if 'crypto_token_id' in kwargs:
            return self.objects.filter(pk= kwargs['crypto_token_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
            
    def add_crypto_token(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_crypto_token"):
            return
        crypto_token=CryptoToken()
        if 'title' in kwargs:
            crypto_token.title= kwargs['title']
        crypto_token.save()
        return crypto_token