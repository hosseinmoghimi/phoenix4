from django import forms

class AddLetterForm(forms.Form):
    title=forms.CharField( max_length=200, required=True)
    sender_id=forms.IntegerField(required=False)
    receiver_id=forms.IntegerField(required=False)