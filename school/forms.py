from django import forms

class SearchForm(forms.Form):
    search_for=forms.CharField( max_length=50, required=True)
class AddSchoolForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)
class AddClassRoomForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)
    school_id=forms.IntegerField( required=True)
class AddMajorForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)