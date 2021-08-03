from core.settings import SITE_URL
from django import forms
from .apps import APP_NAME
from django.shortcuts import reverse
class AddProjectForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50, required=True)

class AddOrganizationUnitForm(forms.Form):
    project_id=forms.IntegerField( required=False)
    organization_unit_id=forms.IntegerField( required=False)
    parent_id=forms.IntegerField(required=False)
    employer_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50, required=True)

class AddMaterialForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50, required=True)
class AddEventForm(forms.Form):
    project_id=forms.IntegerField(required=True)
    event_datetime=forms.CharField( max_length=20, required=False)
    title=forms.CharField(max_length=50, required=True)
class AddMaterialRequestForm(forms.Form):
    project_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    material_id=forms.IntegerField(required=True)
    unit_price=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=50, required=True)

class EditProjectForm(forms.Form):
    project_id=forms.IntegerField(required=True)
    percentage_completed=forms.IntegerField(required=True)
    employer_id=forms.IntegerField(required=False)
    contractor_id=forms.IntegerField(required=False)
    start_date=forms.CharField(max_length=20, required=True)
    end_date=forms.CharField(max_length=20, required=True)
    status=forms.CharField(max_length=50, required=False)
class AddSignatureForm(forms.Form):
    service_request_id=forms.IntegerField(required=False)
    material_request_id=forms.IntegerField(required=False)
    description=forms.CharField(max_length=50,required=False)
    status=forms.CharField(max_length=50,required=True)
class AddEmployeeForm(forms.Form):
    organization_unit_id=forms.IntegerField(required=True)
    profile_id=forms.IntegerField(required=False)
    username=forms.CharField(max_length=50,required=False)
    password=forms.CharField(max_length=50,required=False)
    first_name=forms.CharField(max_length=50,required=False)
    last_name=forms.CharField(max_length=50,required=False)
               
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)
    
class AddLocationForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    new_location=forms.CharField(max_length=500,required=True)
    title=forms.CharField(max_length=500,required=False)
               
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
    service_title=forms.CharField(max_length=150, required=True)
                     