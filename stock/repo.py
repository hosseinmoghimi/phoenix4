from .apps import APP_NAME
from .models import Stock

class StockRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Stock.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
        