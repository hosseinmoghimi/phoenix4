from core.settings import SITE_URL
from django import forms
from .apps import APP_NAME
from django.shortcuts import reverse
class AddProjectForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50, required=True)

class AddOrganizationUnitForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    employer_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50, required=True)

class AddMaterialForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50, required=True)
class AddEventForm(forms.Form):
    project_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=50, required=True)
class AddMaterialRequestForm(forms.Form):
    project_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    material_id=forms.IntegerField(required=True)
    unit_price=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=50, required=True)
               
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)
               
class AddEmployerForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
                  
class AddMaterialForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    parent_id=forms.IntegerField( required=False)
          
class AddServiceForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    parent_id=forms.IntegerField( required=False)
         
class AddServiceRequestForm(forms.Form):
    project_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    unit_price=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=50, required=True)
    service_title=forms.CharField(max_length=50, required=True)
                     