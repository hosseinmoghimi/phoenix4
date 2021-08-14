from messenger.forms import SendMessageForm
from django.http import JsonResponse
from .serializers import MessageSerializer
from rest_framework.views import APIView
from core.constants import FAILED,SUCCEED
from .repo import MessageRepo



class ChannelApi(APIView):
    def send_message(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            send_message_form=SendMessageForm(request.POST)
            if send_message_form.is_valid():
                log=3
                message_title=send_message_form.cleaned_data['message_title']
                message_body=send_message_form.cleaned_data['message_body']
                channel_id=send_message_form.cleaned_data['channel_id']
                event=send_message_form.cleaned_data['event']
                message=MessageRepo(request=request).send_message(
                        message_title=message_title,
                        message_body=message_body,
                        channel_id=channel_id,
                        event=event)
                if message is not None:
                    context['message']=MessageSerializer(message).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)