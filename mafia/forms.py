from django import forms


class CreateGameForm(forms.Form):
    # profile_id=forms.IntegerField(required=False)
    roles=forms.CharField(max_length=500,required=True)
    players=forms.CharField(max_length=500,required=True)

class AddPlayerForm(forms.Form):
    # profile_id=forms.IntegerField(required=False)
    first_name=forms.CharField(max_length=50,required=False)
    last_name=forms.CharField(max_length=50,required=False)
    username=forms.CharField(max_length=50,required=False)
    password=forms.CharField(max_length=50,required=False)
    bio=forms.CharField(max_length=50,required=False)
    mobile=forms.CharField(max_length=50,required=False)
    address=forms.CharField(max_length=200,required=False)
    email=forms.CharField(max_length=50,required=False)