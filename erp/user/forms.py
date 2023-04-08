from django import forms
from .models import UserModel

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = UserModel
        fields = ['username', 'password', 'password2', 'name']