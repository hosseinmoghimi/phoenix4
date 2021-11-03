from django.db.models.fields import BooleanField
from core.settings import SITE_URL
from django import forms
from .apps import APP_NAME
from django.shortcuts import reverse
class AddTaxForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    amount=forms.IntegerField(required=True)
    year=forms.IntegerField(required=True)
