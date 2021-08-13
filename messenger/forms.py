from django import forms

class SendMessageForm(forms.Form):
    message_text=forms.CharField( max_length=100, required=True)
    channel_id=forms.IntegerField(required=True)
    event=forms.CharField( max_length=50, required=False)