# user/views.py
from django.shortcuts import render, redirect
from django.contrib import auth # 사용자 auth 기능
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from django.contrib.auth.hashers import make_password
 
def sign_up_view(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form': form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            form.save()
            return redirect('/sign-in')
        else:
            return render(request, 'user/signup.html', {'form': form})

def sign_in_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            me = auth.authenticate(request, username=username, password=password)
            if me is not None:
                auth.login(request, me)
                return redirect('home')
        else:
            form = LoginForm()
    else:
        form = LoginForm()
        
    return render(request, 'user/signin.html', {'form': form})

@login_required
def logout(request):
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("home")