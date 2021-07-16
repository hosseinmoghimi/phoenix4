from django import forms
class AddContactMessageForm(forms.Form):
    resume_index_id=forms.IntegerField(required=True)
    subject=forms.CharField(max_length=200, required=True)
    email=forms.CharField(max_length=50, required=True)
    mobile=forms.CharField(max_length=13, required=False)
    message=forms.CharField(max_length=500, required=True)
    full_name=forms.CharField(max_length=50, required=True)
    app_name=forms.CharField(max_length=50, required=True)

