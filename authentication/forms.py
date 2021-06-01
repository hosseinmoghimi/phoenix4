from django import forms
class ResetPasswordForm(forms.Form):
    username=forms.CharField(required=True,max_length=200)
    old_password=forms.CharField(max_length=150, required=False)
    new_password=forms.CharField(max_length=150, required=True)

class LoginForm(forms.Form):
    username=forms.CharField(max_length=50, required=True)
    password=forms.CharField(max_length=150, required=True)
    back_url=forms.CharField(max_length=150, required=False)
class RegisterForm(forms.Form):
    username=forms.CharField(max_length=50, required=True)
    password=forms.CharField(max_length=150, required=True)
    first_name=forms.CharField(max_length=50, required=True)
    last_name=forms.CharField(max_length=50, required=True)
