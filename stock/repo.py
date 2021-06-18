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
        if 'agent_id' in kwargs:
            objects=objects.filter(agent_id=kwargs['agent_id'])
        return objects
        

    def stock(self,*args, **kwargs):
        pk=0
        if 'stock_id' in kwargs:
            pk=kwargs['stock_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
        