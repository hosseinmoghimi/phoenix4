from django import forms

class DoKoshtarForm(forms.Form):
    tag=forms.CharField(max_length=50, required=True)
    koshtar_date=forms.CharField(max_length=50,required=False)
    # price=forms.IntegerField(required=False)
    weight=forms.FloatField(required=False)
    Jegar_price=forms.IntegerField(required=False)
    Kalle_pache_price=forms.IntegerField(required=False)
    pust_price=forms.IntegerField(required=False)
    transport_fee=forms.IntegerField(required=False)
    koshtar_fee=forms.IntegerField(required=False)
    lashe_price=forms.IntegerField(required=False)
    lashe_weight=forms.FloatField(required=False)
    description = forms.CharField(required=False,max_length=500)
 
class AddNewAnimalForm(forms.Form):
    category=forms.CharField(max_length=50, required=True)
    saloon_id=forms.IntegerField(required=True)
    tag=forms.CharField(max_length=50, required=True)
    price=forms.IntegerField(required=False)
    weight=forms.FloatField(required=False)
    enter_date=forms.CharField(max_length=50,required=False)
class EnterAnimalToSaloonForm(forms.Form):
    saloon_id=forms.IntegerField(required=True)
    animal_id=forms.IntegerField(required=False)
    animal_tag=forms.IntegerField(required=False)
    animal_price=forms.IntegerField(required=False)
    animal_weight=forms.IntegerField(required=False)
    enter_date=forms.CharField(max_length=50, required=True)
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