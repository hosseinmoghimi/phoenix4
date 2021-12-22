from django.db.models.fields import BooleanField
from core.settings import SITE_URL
from django import forms
from .apps import APP_NAME
from django.shortcuts import reverse
class AddBookForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    shelf=forms.CharField(max_length=100, required=True)
    col=forms.CharField(max_length=100, required=True)
    row=forms.CharField(max_length=100, required=True)
    year=forms.IntegerField(required=True)
    price=forms.IntegerField(required=True)
    description=forms.CharField(max_length=1000, required=False)


class AddMemberForm(forms.Form):
    profile_id=forms.IntegerField(required=True)
    description=forms.CharField(max_length=1000, required=False)
    level=forms.CharField(max_length=50, required=False)

class LendBookForm(forms.Form):
    member_id=forms.IntegerField(required=True)
    book_id=forms.IntegerField(required=True)
    description=forms.CharField(max_length=1000, required=False)
   
class DeliverBookForm(forms.Form):
    book_id=forms.IntegerField(required=True)
    description=forms.CharField(max_length=1000, required=False)
   