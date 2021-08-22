from .models import Relay

class RelayRepo:
    def __init__(self,*args, **kwargs):
        self.objects=Relay.objects
    