from django import forms

class StartGameForm(forms.Form):
    game_id=forms.IntegerField(required=True)

class NewVoteForm(forms.Form):
    day_id=forms.IntegerField(required=True)
    accused_id=forms.IntegerField(required=True)
    level=forms.IntegerField(required=True)
    
class StartGameDayForm(forms.Form):
    game_id=forms.IntegerField(required=True)
    # counter=forms.IntegerField(required=True)
    
class EndGameDayForm(forms.Form):
    game_day_id=forms.IntegerField(required=True)
    
class EndGameNightForm(forms.Form):
    game_night_id=forms.IntegerField(required=True)
    
class StartGameNightForm(forms.Form):
    game_id=forms.IntegerField(required=True)
    # counter=forms.IntegerField(required=True)

class ShuffleGameForm(forms.Form):
    game_id=forms.IntegerField(required=True)
class CreateGameForm(forms.Form):
    god_id=forms.IntegerField(required=True)
    scenario=forms.CharField(max_length=50,required=False)
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