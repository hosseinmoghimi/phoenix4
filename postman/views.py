import json
from django.shortcuts import render
from .forms import *
from .serializers import LetterSerializer
from .repo import LetterRepo
from .apps import APP_NAME
from core.views import CoreContext, PageContext
from django.views import View
TEMPLATE_ROOT="postman/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
# Create your views here.
class BasicView(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        letters=LetterRepo(request=request).list(*args, **kwargs)
        if request.user.has_perm(APP_NAME+".add_letter"):
            context['add_letter_form']=AddLetterForm()
        context['letters']=letters
        context['letters_s']=json.dumps(LetterSerializer(letters,many=True).data)
        return render(request,TEMPLATE_ROOT+"index.html",context)

class LetterViews(View):
    def letter(self,request,*args, **kwargs):
        context=getContext(request=request)
        letter=LetterRepo(request=request).letter(*args, **kwargs)
        context.update(PageContext(request=request,page=letter))
        context['letter']=letter
        return render(request,TEMPLATE_ROOT+"letter.html",context)
    def letters(self,request,*args, **kwargs):
        context=getContext(request=request)
        letters=LetterRepo(request=request).list(*args, **kwargs)
        context['letters']=letters
        context['letters_s']=json.dumps(LetterSerializer(letters,many=True).data)
        if request.user.has_perm(APP_NAME+".add_letter"):
            context['add_letter_form']=AddLetterForm()
        return render(request,TEMPLATE_ROOT+"letters.html",context)