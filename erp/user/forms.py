from django import forms
from django.contrib.auth import get_user_model
from django.contrib import auth

UserModel = get_user_model()

class SignUpForm(forms.ModelForm):
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'name']
        labels = {'username':'아이디',
                  'password':'비밀번호',
                  'name':'이름'
                  }
        
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

class SignInForm(forms.Form):
    username = forms.CharField(label='아이디', max_length=30)
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)


    
