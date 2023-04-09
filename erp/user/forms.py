from django import forms
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class SignUpForm(forms.ModelForm):
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'name']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
