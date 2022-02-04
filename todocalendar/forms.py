from django import forms

class AddAppointmentForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    title=forms.CharField(max_length=100, required=True)
class AddPersonForm(forms.Form):
    profile_id=forms.IntegerField(required=True)
    appointment_id=forms.IntegerField(required=True)