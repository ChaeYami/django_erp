# user/views.py
 
from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
 
from django.contrib import auth # 사용자 auth 기능
from django.contrib.auth import get_user_model #사용자가 있는지 검사하는 함수
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignupForm
 
def sign_up_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            name = form.cleaned_data.get('name')
            if password != password2:
                return render(request, 'user/signup.html', {'form': form, 'error': '비밀번호가 일치하지 않습니다.'})
            else:
                user, created = get_user_model().objects.get_or_create(username=username)
                if created:
                    user.set_password(password)
                    user.name = name
                    user.save()
                    return redirect('/sign-in')
                else:
                    return render(request, 'user/signup.html', {'form': form, 'error': '이미 존재하는 사용자입니다.'})
        else:
            return render(request, 'user/signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'user/signup.html', {'form': form})

 
def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
 
        me = auth.authenticate(request, username=username, password=password)  # 사용자 불러오기
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('/')
        else:
            return redirect('/sign-in')  # 로그인 실패
    elif request.method == 'GET':
        return render(request, 'user/signin.html')

@login_required
def logout(request):
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("/")