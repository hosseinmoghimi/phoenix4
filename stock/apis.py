from core.constants import FAILED,SUCCEED
from stock.serializers import DocumentSerializer
from rest_framework.views import APIView
from .repo import DocumentRepo
from .forms import AddDocumentForm
from django.http import JsonResponse

class DocumentApi(APIView):
    def add_document(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_project_form=AddDocumentForm(request.POST,request.FILES)
            if add_project_form.is_valid():
                log+=1
                title=add_project_form.cleaned_data['title']
                stock_id=add_project_form.cleaned_data['stock_id']
                file=request.FILES['file']      
                document=DocumentRepo(request=request).add_document(title=title,stock_id=stock_id,file=file)
                context['document']=DocumentSerializer(document).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)