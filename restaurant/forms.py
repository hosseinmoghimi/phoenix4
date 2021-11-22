from django import forms

class AddFoodForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
class ServeMealForm(forms.Form):
    guest_id=forms.IntegerField(required=True)
    meal_id=forms.IntegerField(required=True)
class ReserveMealForm(forms.Form):
    meal_id=forms.IntegerField(required=True)
    guest_id=forms.IntegerField(required=True)