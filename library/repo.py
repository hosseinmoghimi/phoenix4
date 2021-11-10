from django.db.models.aggregates import Avg
from django.utils import timezone
from authentication.repo import ProfileRepo
from django.db.models import Q,Sum
from .apps import APP_NAME
from .models import Book
from core.repo import ParameterRepo
from .enums import ParametersEnum

def show_archives(request):
        parameter_repo = ParameterRepo(request=request,app_name=APP_NAME)
        show_archives=parameter_repo.parameter(ParametersEnum.SHOW_ARCHIVES).boolesan_value
        return show_archives
class BookRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=Book.objects.all()
        
        if_show_archives=show_archives(request=self.request)
        self.objects=self.objects.all()
        if not if_show_archives:
            self.objects=self.objects.filter(archive=False)
          

    def book(self, *args, **kwargs):
        
        if 'book_id' in kwargs:
            pk=kwargs['book_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_book(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_book"):
            return 

        book=Book()

        if 'title' in kwargs:
            book.title=kwargs['title']

        if 'description' in kwargs:
            book.description=kwargs['description']

        if 'year' in kwargs:
            book.year=kwargs['year']


        if 'price' in kwargs:
            book.price=kwargs['price']

        if 'shelf' in kwargs:
            book.shelf=kwargs['shelf']

        if 'row' in kwargs:
            book.row=kwargs['row']


        if 'col' in kwargs:
            book.col=kwargs['col']
        book.save()
        return book
