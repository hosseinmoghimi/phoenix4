from authentication.repo import ProfileRepo
from .apps import APP_NAME
from .models import Agent, Document, Payment, Stock
from django.db.models import Q


class AgentRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Agent.objects
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'agent_id' in kwargs:
            objects=objects.filter(agent_id=kwargs['agent_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(profile__user__first_name__contains=search_for)
            |Q(profile__user__last_name__contains=search_for)
            # |Q(stock1=search_for)
            # |Q(stock2=search_for)
            )
        return objects
        

    def agent(self,*args, **kwargs):
        pk=0
        if 'agent_id' in kwargs:
            pk=kwargs['agent_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

        
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
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(profile__user__first_name__contains=search_for)
            |Q(profile__user__last_name__contains=search_for)
            # |Q(stock1=search_for)
            # |Q(stock2=search_for)
            )
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
    def add_stock(self,*args, **kwargs):
        first_name=kwargs['first_name']
        last_name=kwargs['last_name']
        stock1=kwargs['stock1'] if 'stock1' in kwargs else 0
        stock2=kwargs['stock2'] if 'stock2' in kwargs else 0
        agent_id=kwargs['agent_id'] if 'agent_id' in kwargs else 1
        if self.user.has_perm(APP_NAME+".add_stock"):
            stock=Stock()
            from django.contrib.auth.models import User
            import random
            aaa=random.randint(1000,9999)
            username="user"+str(aaa)
            bbb=random.randint(1000,9999)
            password="pass@"+str(bbb)
            user=User.objects.create(username=username,password=password,first_name=first_name,last_name=last_name)
            profile=ProfileRepo(user=user).me
            stock.profile=profile
            stock.stock1=stock1
            stock.stock2=stock2
            stock.agent_id=agent_id
            stock.save()
            return stock

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
        