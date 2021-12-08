from django import forms

class AddFoodForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
class AddHostForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    profile_id=forms.IntegerField(required=True)
class ServeMealForm(forms.Form):
    guest_id=forms.IntegerField(required=True)
    meal_id=forms.IntegerField(required=True)
class ReserveMealForm(forms.Form):
    meal_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=False)
    guest_id=forms.IntegerField(required=False)
class AddMealForm(forms.Form):
    food_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=False)
    host_id=forms.IntegerField(required=True)
class UnreserveMealForm(forms.Form):
    meal_id=forms.IntegerField(required=True)
    guest_id=forms.IntegerField(required=False)