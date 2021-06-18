from .apps import APP_NAME
from .models import Stock

class StockRepo:
    def __init__(self,*args, **kwargs):
        self.objects=Stock.objects
        