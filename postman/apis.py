from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from .repo import LetterRepo
from django.http import JsonResponse
from .forms import *
from .serializers import LetterSerializer


class LetterApi(APIView):
    def add_letter(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            add_letter_form=AddLetterForm(request.POST)
            if add_letter_form.is_valid():
                fm=add_letter_form.cleaned_data
                title=fm['title']
                letter=LetterRepo(request=request).add_letter(title=title)
                if letter is not None:
                    context['letter']=LetterSerializer(letter).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
