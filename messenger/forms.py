from django import forms

class SendMessageForm(forms.Form):
    message_title=forms.CharField( max_length=100, required=False)
    message_body=forms.CharField( max_length=100, required=True)
    channel_id=forms.IntegerField(required=True)
    event=forms.CharField( max_length=50, required=False)
    
class SendNotificationForm(forms.Form):
    message_title=forms.CharField( max_length=100, required=False)
    message_body=forms.CharField( max_length=100, required=True)
    member_id=forms.IntegerField(required=True)