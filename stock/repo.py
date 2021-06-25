from .apps import APP_NAME
from .models import Document, Payment, Stock

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
        
class DocumentRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Document.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'agent_id' in kwargs:
            objects=objects.filter(agent_id=kwargs['agent_id'])
        return objects
    def add_document(self,*args, **kwargs):
        if self.user.has_perm(APP_NAME+".add_document"):
            document=Document(*args, **kwargs)
            document.save()
            return document
            

    def document(self,*args, **kwargs):
        pk=0
        if 'document_id' in kwargs:
            pk=kwargs['document_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
             
class PaymentRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Payment.objects

    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'agent_id' in kwargs:
            objects=objects.filter(agent_id=kwargs['agent_id'])
        return objects
    def add_payment(self,*args, **kwargs):
        if self.user.has_perm(APP_NAME+".add_payment"):
            payment=Payment(*args, **kwargs)
            payment.save()
            return payment
            

    def document(self,*args, **kwargs):
        pk=0
        if 'document_id' in kwargs:
            pk=kwargs['document_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
        