from django import forms


class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)
    
class AddNewAnimalForm(forms.Form):
    category=forms.CharField(max_length=50, required=True)
    saloon_id=forms.IntegerField(required=True)
    tag=forms.CharField(max_length=50, required=True)
    price=forms.IntegerField(required=False)
    weight=forms.FloatField(required=False)
    enter_date=forms.CharField(max_length=50,required=False)
class EnterAnimalToSaloonForm(forms.Form):
    animal_id=forms.IntegerField(required=True)
    saloon_id=forms.IntegerField(required=True)
    animal_price=forms.IntegerField(required=False)
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)
    
    animal_weight=forms.FloatField(required=False)
    enter_date=forms.CharField(max_length=50,required=False)
class SaloonDailyReportForm(forms.Form):
    saloon_id=forms.IntegerField(required=True)
    report_date=forms.CharField(max_length=50,required=False)
class AddCostForm(forms.Form):
    employee_id=forms.IntegerField(required=True)
    saloon_id=forms.IntegerField(required=True)
    value=forms.IntegerField(required=True)
    cost_date=forms.CharField(max_length=50,required=False)
    title=forms.CharField(max_length=50,required=False)
    category=forms.CharField(max_length=50,required=False)